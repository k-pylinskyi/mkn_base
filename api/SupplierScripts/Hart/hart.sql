SELECT DISTINCT
            24 AS supplier_id,
            data.hart_part_number,
            data.part_number,
            data.manufacturer,
            data.part_name,
            REPLACE(quantity.qty, '>', '') AS quantity,
            IIF(deposit.price is null, prices.price, prices.price + ROUND(deposit.price, 2)) AS final_price
            data.unit_measure,
            weight.weight,
            cn.tariff_code,
            data.ean_code,
            data.origin
            FROM data
            INNER JOIN prices
            ON data.hart_part_number = prices.hart_part_number
            INNER JOIN quantity
            ON data.hart_part_number = quantity.hart_part_number
            LEFT JOIN deposit
            ON data.hart_part_number = deposit.hart_part_number
            INNER JOIN weight
            ON data.hart_part_number = weight.hart_part_number
            WHERE
            quantity.warehouse in('V', 'S', '1')