param(
	[string]$password = "c4dc3571c4794f10b3d7ba8c8d83e50f"
)

$env:PGPASSWORD = $password
& psql -U postgres
c4dc3571c4794f10b3d7ba8c8d83e50f