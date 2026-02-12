-- Создание таблиц

CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    registration_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS energy_supply_points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    connection_date DATE NOT NULL,
    max_power_kw DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS company_clients (
    id SERIAL PRIMARY KEY,
    energy_supply_point_id INTEGER NOT NULL REFERENCES energy_supply_points(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    quantity_power DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Возвращает статистику по компании
CREATE OR REPLACE FUNCTION get_company_statistics(p_company_id INTEGER)
RETURNS TABLE (
    total_supply_points INTEGER,
    max_total_power DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INTEGER AS total_supply_points,
        COALESCE(SUM(max_power_kw), 0)::DECIMAL AS max_total_power
    FROM energy_supply_points
    WHERE company_id = p_company_id;
END;
$$ LANGUAGE plpgsql;

-- Логика аренды мощностей
CREATE OR REPLACE FUNCTION rent_energy(
    p_energy_supply_point_id INTEGER,
    p_company_name VARCHAR,
    p_quantity_power DECIMAL
)
RETURNS TABLE (
    success BOOLEAN,
    message TEXT
) AS $$
DECLARE
    v_max_power DECIMAL;
    v_used_power DECIMAL;
    v_available_power DECIMAL;
BEGIN
    -- Получаем максимальную мощность точки поставки
    SELECT max_power_kw INTO v_max_power
    FROM energy_supply_points
    WHERE id = p_energy_supply_point_id;
    
    -- Проверяем существование точки поставки
    IF v_max_power IS NULL THEN
        RETURN QUERY SELECT FALSE, 'Energy supply point not found';
        RETURN;
    END IF;
    
    -- Получаем уже использованную мощность
    SELECT COALESCE(SUM(quantity_power), 0) INTO v_used_power
    FROM company_clients
    WHERE energy_supply_point_id = p_energy_supply_point_id;
    
    -- Вычисляем доступную мощность
    v_available_power := v_max_power - v_used_power;
    
    -- Проверяем наличие свободной мощности
    IF v_available_power < p_quantity_power THEN
        RETURN QUERY SELECT 
            FALSE, 
            'Insufficient power. Available: ' || v_available_power::TEXT || ' kW, Requested: ' || p_quantity_power::TEXT || ' kW';
        RETURN;
    END IF;
    
    -- Создаем запись в таблице company_clients
    INSERT INTO company_clients (energy_supply_point_id, company_name, quantity_power)
    VALUES (p_energy_supply_point_id, p_company_name, p_quantity_power);
    
    RETURN QUERY SELECT TRUE, 'Energy rented successfully';
END;
$$ LANGUAGE plpgsql;

-- Поиск точек поставки по дате присоединения
CREATE OR REPLACE FUNCTION search_energy_supply_points(
    p_connection_date_from DATE DEFAULT NULL,
    p_connection_date_to DATE DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    company_id INTEGER,
    connection_date DATE,
    max_power_kw DECIMAL,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        esp.id,
        esp.name,
        esp.company_id,
        esp.connection_date,
        esp.max_power_kw,
        esp.created_at
    FROM energy_supply_points esp
    WHERE 
        (p_connection_date_from IS NULL OR esp.connection_date >= p_connection_date_from)
        AND (p_connection_date_to IS NULL OR esp.connection_date <= p_connection_date_to)
    ORDER BY esp.connection_date;
END;
$$ LANGUAGE plpgsql;

-- Вставка тестовых данных
INSERT INTO companies (name, registration_date, status) VALUES
    ('ЭнергоПром', '2020-01-15', 'active'),
    ('СилаТок', '2021-03-20', 'active'),
    ('МегаВатт', '2019-11-10', 'inactive');

INSERT INTO energy_supply_points (name, company_id, connection_date, max_power_kw) VALUES
    ('Точка А1', 1, '2020-02-01', 1000.00),
    ('Точка А2', 1, '2020-05-15', 1500.00),
    ('Точка Б1', 2, '2021-04-01', 2000.00),
    ('Точка В1', 3, '2020-01-10', 500.00);

INSERT INTO company_clients (energy_supply_point_id, company_name, quantity_power) VALUES
    (1, 'Клиент 1', 300.00),
    (1, 'Клиент 2', 200.00),
    (2, 'Клиент 3', 500.00);
