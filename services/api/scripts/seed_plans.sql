INSERT INTO plans (id, code, name, monthly_price_brl, active)
VALUES
    ('10000000-0000-0000-0000-000000000001', 'free', 'Free', 0, true),
    ('10000000-0000-0000-0000-000000000002', 'solo', 'Solo', 2900, true),
    ('10000000-0000-0000-0000-000000000003', 'pro', 'Pro', 7900, true)
ON CONFLICT (code) DO UPDATE
SET
    name = EXCLUDED.name,
    monthly_price_brl = EXCLUDED.monthly_price_brl,
    active = EXCLUDED.active;
