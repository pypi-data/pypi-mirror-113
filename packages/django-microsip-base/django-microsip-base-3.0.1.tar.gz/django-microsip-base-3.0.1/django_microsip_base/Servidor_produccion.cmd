echo off
color 3F
cls
echo 			==================================
echo 			=                                =
echo 			=     SERVIDOR DE PAGINA WEB     =
echo 			=                                =
echo 			=     MODO: PRODUCCION           =
echo 			=     POR FAVOR NO CERRAR !!!!   =
echo 			=                                =
echo 			==================================
echo.
echo.

python manage_prod.py runserver_plus 0.0.0.0:8001 --insecure
