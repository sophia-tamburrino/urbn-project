DROP TABLE IF EXISTS users;
CREATE TABLE users (
  email        varchar(50) not null PRIMARY KEY,
  name       varchar(50) not null,
  password       varchar(50) not null
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
  name varchar(50) not null PRIMARY KEY
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  id        int(4) not null PRIMARY KEY,
  title        varchar(50) not null,
  price        float(4) not null,
  stock        int(4) not null,
  cat        varchar(50) not null,
  pic       varchar(50) not null,
  foreign key (cat) references category(name)
);

DROP TABLE IF EXISTS user_order;
CREATE TABLE user_order (
    order_id int(4) not null PRIMARY KEY,
    customer_email varchar(50) not null,
    order_date date,
    total float(4),
    foreign key (customer_email) references user(email)
);

DROP TABLE IF EXISTS orderitem;
CREATE TABLE orderitem (
    order_id int(4) not null,
    customer_email varchar(50) not null,
    order_date date,
    product_id int(4),
    quantity id(4),
    foreign key (order_id) references user_order(order_id),
    foreign key (customer_email) references user_order(customer_email),
    foreign key (order_date) references user_order(order_date),
    foreign key (product_id) references product(id)
);

--- Users
INSERT INTO users VALUES ('user@email.com', 'Sophia', 'fakepassword123');
INSERT INTO users VALUES ('testuser@email.com', 'meow', 'testpass');
--- Category
INSERT INTO category VALUES ('Nintendo Switch');
INSERT INTO category VALUES ('PlayStation 5');
INSERT INTO category VALUES ('PC');

--- Products
INSERT INTO product VALUES (1, 'Legend of Zelda: Tears of the Kingdom', 40, 15, 'Nintendo Switch', 'zelda.png');
INSERT INTO product VALUES (2, 'Splatoon 3', 40, 15, 'Nintendo Switch', 'splatoon.png');
INSERT INTO product VALUES (3, 'Animal Crossing New Horizons', 40, 15, 'Nintendo Switch', 'acnh.png');
INSERT INTO product VALUES (4, 'Hollow Knight', 40, 15, 'Nintendo Switch', 'hollow.png');
INSERT INTO product VALUES (5, 'Hello Kitty Island Adventure', 40, 15, 'Nintendo Switch', 'hellokitty.png');
INSERT INTO product VALUES (6, 'Crow Country', 40, 15, 'Nintendo Switch', 'crow.png');
INSERT INTO product VALUES (7, 'Signalis', 40, 15, 'Nintendo Switch', 'signalis.png');

INSERT INTO product VALUES (8, 'Monster Hunter Wilds', 40, 15, 'PlayStation 5', 'mhw.png');
INSERT INTO product VALUES (9, 'Ghost of Tsushima', 40, 15, 'PlayStation 5', 'ghost.png');
INSERT INTO product VALUES (10, 'Persona 5', 40, 15, 'PlayStation 5', 'p5.png');
INSERT INTO product VALUES (11, 'Minecraft', 40, 15, 'PlayStation 5', 'mine.png');

INSERT INTO product VALUES (12, 'Hades', 40, 15, 'PC', 'hades.png');
INSERT INTO product VALUES (13, 'Ori and the Blind Forest', 40, 15, 'PC', 'ori.png');
INSERT INTO product VALUES (14, 'Wizard101', 40, 15, 'PC', 'wizard.png');
INSERT INTO product VALUES (15, 'Lethal Company', 40, 15, 'PC', 'lethal.png');
INSERT INTO product VALUES (16, 'Project Zomboid', 40, 15, 'PC', 'zomboid.png');
INSERT INTO product VALUES (17, 'Keep Talking and Nobody Explodes', 40, 15, 'PC', 'ktne.png');

--- User Order
INSERT INTO user_order VALUES (1, 'user@email.com', '2025-03-23', 120);

--- Order Item
INSERT INTO orderitem VALUES (1, 'user@email.com', '2025-03-23', 1, 2);
INSERT INTO orderitem VALUES (1, 'user@email.com', '2025-03-23', 2, 1);