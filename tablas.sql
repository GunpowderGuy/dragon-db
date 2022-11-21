-- tablas de personas
CREATE TABLE Persona (
    DNI bigint NOT NULL PRIMARY KEY,
    Apellidos varchar(50) NOT NULL,
    Nombre varchar(50) NOT NULL
);

CREATE TABLE Trabajador (  
    DNI bigint NOT NULL PRIMARY KEY ,
    Sueldo int NOT NULL,
    Turno varchar(10) NOT NULL,
    fecha_inicio_tra date not NULL,
    fecha_fin_tra date ,
    constraint FK_TrabajadorDNI FOREIGN KEY (DNI) REFERENCES Persona(DNI)

);

CREATE TABLE Vendedor(
    DNI int NOT NULL PRIMARY KEY ,
    constraint FK_VendedorDNI FOREIGN KEY (DNI) REFERENCES Trabajador(DNI)
);

CREATE TABLE Instalador(
    DNI bigint NOT NULL PRIMARY KEY ,
    constraint FK_InstaladorDNI FOREIGN KEY (DNI) REFERENCES Trabajador(DNI)
);

CREATE TABLE Cliente (
    DNI bigint NOT NULL PRIMARY KEY ,
    constraint FK_ClienteDNI FOREIGN KEY (DNI) REFERENCES Persona(DNI)

);

-- Tabla del producto

CREATE TABLE Producto(
    Nombre varchar(50) NOT NULL PRIMARY KEY,
    Tipo varchar(20) NOT NULL
);

-- Tabla de Organización

CREATE TABLE Organizacion(
    RUC bigint NOT NULL PRIMARY KEY,
    Nombre varchar(50)NOT NULL,
    Tipo varchar(20)NOT NULL
);
-- Tablas de Venta
CREATE TABLE Venta(
    idCompra varchar(10) NOT NULL PRIMARY KEY,
    VendedorID bigint NOT NULL,
    Direccion varchar(250)NOT NULL,
    constraint FK_VentaVendedorID FOREIGN KEY (VendedorID) REFERENCES Vendedor(DNI)
);

CREATE TABLE VentaCorta (
    idCompra varchar(10) not NULL PRIMARY KEY,
    ClienteID bigint NOT NULL,
    constraint FK_idCompraVC FOREIGN KEY (idCompra) REFERENCES Venta(idCompra),
    constraint FK_ClienteDNIVC FOREIGN KEY (ClienteID) REFERENCES Cliente(DNI)
);

CREATE TABLE VentaLarga(
    idCompra varchar(10) not NULL PRIMARY KEY,
    OrganizacionRuc bigint NOT NULL,
    Duracion_estimada  int NOT NULL,
    constraint FK_idCompraVL FOREIGN KEY (idCompra) REFERENCES Venta(idCompra),
    constraint FK_RUC FOREIGN KEY (OrganizacionRuc)  REFERENCES Organizacion(RUC)

);

CREATE TABLE Instalacion(
    VentaID varchar(10) NOT NULL,
    Fecha_instalacion date NOT NULL,
    InstaladorDNI bigint NOT NULL,
    constraint FK_VentaIDI FOREIGN KEY (VentaID) REFERENCES Venta(idCompra),
    constraint FK_InstaladorDNIIDI FOREIGN KEY (InstaladorDNI) REFERENCES Instalador(DNI),

    constraint PK_I PRIMARY KEY (VentaID,Fecha_instalacion,InstaladorDNI)
);


CREATE TABLE necesita_usar  (
    VentaID varchar(10) not NULL,
    ProductoN varchar(50) not NULL,
    Cantidad int NOT NULL,
    constraint FK_VentaID FOREIGN KEY (VentaID) REFERENCES Venta(idCompra),
    constraint FK_Producto FOREIGN KEY (ProductoN) REFERENCES Producto(Nombre),
    constraint PK_NU PRIMARY KEY(VentaID,ProductoN)
);


CREATE TABLE Gerenciado_por(
    Gerente bigint NOT NULL,
    Gerenciado bigint NOT NULL,
    constraint PK_Gerenciado_por PRIMARY KEY (Gerente,Gerenciado),
    constraint FK_GerenteGP FOREIGN KEY (Gerente) REFERENCES Trabajador(DNI),
    constraint FK_GerenciadoGP FOREIGN KEY (Gerenciado) REFERENCES Trabajador(DNI)

);