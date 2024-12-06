# Input and output file paths
$inputFile = "ticketing_db_full.sql"
$outputFile = "ticketing_db_full_cleaned.sql"

# Read the original file, clean up each line, and save only valid SQL to the output
(Get-Content $inputFile) | ForEach-Object {
    if ($_ -notmatch '^SET ' `
        -and $_ -notmatch 'OWNER TO' `
        -and $_ -notmatch 'CREATE SEQUENCE' `
        -and $_ -notmatch 'ALTER SEQUENCE' `
        -and $_ -notmatch '^COPY ' `
        -and $_ -notmatch '^\\\.' `
        -and $_ -notmatch 'pg_catalog.set_config' `
        -and $_ -notmatch 'pg_catalog.setval' `
        -and $_ -notmatch 'ADD CONSTRAINT' `
        -and $_ -notmatch 'ALTER TABLE .* ALTER COLUMN' `
        -and $_ -notmatch 'START WITH.*INCREMENT BY.*' `
        -and $_ -notmatch '^[0-9]+ .*' `
        -and $_ -notmatch '^--') {
            $_ -replace 'CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ' `
               -replace 'AS integer.*', '' `
               -replace 'ALTER TABLE ONLY', 'ALTER TABLE' `
               -replace '::character varying', '' `
               -replace '::integer', '' `
               -replace 'SERIAL', 'INTEGER PRIMARY KEY AUTOINCREMENT' `
               -replace 'DEFAULT nextval\(.*\)', '' `
               -replace 'public\.', ''
    }
} | Set-Content $outputFile

Write-Host "SQL cleanup completed. Cleaned file saved as $outputFile."
