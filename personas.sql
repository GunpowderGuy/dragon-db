--peronas dni apellidos nombre
--para instalador
insert into persona (dni,apellidos,nombre) values(56981582,'Cisneros','Ana');
insert into persona (dni,apellidos,nombre) values(98548293,'Ramirez','Cesar');
insert into persona (dni,apellidos,nombre) values(43238999,'Barraza','Cristobal');
insert into persona (dni,apellidos,nombre) values(29405006,'Rojas','Juana');
insert into persona (dni,apellidos,nombre) values(50560345,'Rincon','Lili');

--para vendedor
insert into persona (dni,apellidos,nombre) values(50560365,'Sandoval','Miriam');
insert into persona (dni,apellidos,nombre) values(90542850,'Tejeda','Ana');
insert into persona (dni,apellidos,nombre) values(51029504,'Riojas','Esther');
insert into persona (dni,apellidos,nombre) values(74548110,'Becerra','James');
insert into persona (dni,apellidos,nombre) values(73123844,'Baltazar','Juan');

--insertar en trabajador

INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (56981582,2700,'Dia','2019-05-12', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (98548293,2700,'Tarde','2019-06-10', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (43238999,2700,'Noche','2019-07-14', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (29405006,2700,'Dia','2019-04-13', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (50560345,2700,'Tarde','2019-08-14', NULL);

INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (50560365,2700,'Noche','2019-02-17', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (90542850,2700,'Dia','2019-09-18', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (51029504,2700,'Tarde','2019-08-19', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (74548110,2700,'Noche','2019-06-12', NULL);
INSERT INTO trabajador(dni,sueldo,turno,fecha_inicio_tra,fecha_fin_tra) values (73123844,2700,'Dia','2019-11-11', NULL);

-- insetar en instalador
INSERT INTO instalador(dni) values (56981582);
INSERT INTO instalador(dni) values (98548293);
INSERT INTO instalador(dni) values (43238999);
INSERT INTO instalador(dni) values (29405006);
INSERT INTO instalador(dni) values (50560345);

--insertar en vendedor
INSERT INTO vendedor(dni) values (50560365);
INSERT INTO vendedor(dni) values (90542850);
INSERT INTO vendedor(dni) values (51029504);
INSERT INTO vendedor(dni) values (74548110);
INSERT INTO vendedor(dni) values (73123844);