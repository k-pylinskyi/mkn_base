SELECT
data.main_part_number,
data.manufacturer,
data.category,
data.origin,
price.price,
IFNULL(deposit.deposit, 0) AS deposit, quantity.warehouse,
REPLACE(quantity.quantity, '>', '') AS quantity,
(price.price + IFNULL(deposit.deposit, 0)) AS final_price
FROM data
INNER JOIN price ON  data.part_number = price.part_number
INNER JOIN quantity ON data.part_number = quantity.part_number
LEFT JOIN deposit ON data.part_number = deposit.part_number
WHERE
price.price > 2
AND (quantity.warehouse = 'A' OR quantity.warehouse = 'H' OR quantity.warehouse = 'J' OR
quantity.warehouse = '3' OR quantity.warehouse = '9')
AND (price.price + IFNULL(deposit.deposit, 0)) > 2;