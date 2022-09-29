CREATE VIEW IF NOT EXISTS suppliers_prices AS
SELECT
suppliers.name AS supplier_name,
suppliers.currency,
autopartner_gdansk.manufacturer,
autopartner_gdansk.supplier_part_number,
autopartner_gdansk.part_number,
autopartner_gdansk.price,
autopartner_gdansk.quantity
FROM suppliers
INNER JOIN autopartner_gdansk
ON suppliers.id = autopartner_gdansk.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
emoto.manufacturer,
emoto.supplier_part_number,
emoto.part_number,
emoto.price,
emoto.quantity
FROM suppliers
INNER JOIN emoto
ON suppliers.id = emoto.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
gordon.manufacturer,
gordon.supplier_part_number,
gordon.part_number,
gordon.price,
gordon.quantity
FROM suppliers
INNER JOIN gordon
ON suppliers.id = gordon.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
motorol.manufacturer,
motorol.supplier_part_number,
motorol.part_number,
motorol.price,
motorol.quantity
FROM suppliers
INNER JOIN motorol
ON suppliers.id = motorol.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
paketo.manufacturer,
paketo.supplier_part_number,
paketo.part_number,
paketo.price,
paketo.quantity
FROM suppliers
INNER JOIN paketo
ON suppliers.id = paketo.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
hart.manufacturer,
hart.supplier_part_number,
hart.part_number,
hart.price,
hart.quantity
FROM suppliers
INNER JOIN hart
ON suppliers.id = hart.supplier_id

UNION

SELECT
suppliers.name AS supplier_name,
suppliers.currency,
rodon.manufacturer,
rodon.supplier_part_number,
rodon.part_number,
rodon.price,
rodon.quantity
FROM suppliers
INNER JOIN rodon
ON suppliers.id = rodon.supplier_id
