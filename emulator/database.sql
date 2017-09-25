-- create database mgsv_server;
use mgsv_server;
create table if not exists players(
	id int not null auto_increment,
						-- there is no point in saving steam_ticket since it renews every time
	steam_id varchar(17), 			-- from server CMD_AUTH_STEAMTICKET, 17-chars steamid
	currency varchar(4),			-- from server CMD_AUTH_STEAMTICKET, 2-3 letter currency, not sure if it can be 4 letters
	password varchar(32),			-- from server CMD_AUTH_STEAMTICKET, loginid_password, base64
	smart_device_id varchar(128),		-- from server CMD_AUTH_STEAMTICKET, smart_device_id, base64
	magic_hash varchar(32), 		-- from client CMD_REQAUTH_HTTPS   , base64 hash from client
	crypto_key varchar(32), 		-- from server CMD_REQAUTH_HTTPS   , blowfish crypto key used for encrypting session messages
	last_login datetime,			-- date of last login
	last_command datetime,			-- date of last received command from client
	session_id varchar(32),			-- session identifier used for further communications, expires if there was no commands for client for 2 mins
	client_ip varchar(16), 			-- client ip, can be used for static authentication
	ex_ip varchar(16), 				-- from client CMD_SEND_IPANDPORT
	ex_port varchar(7),
	in_ip varchar(16),
	in_port varchar(7),
	nat varchar(48),
	xnaddr varchar(48), 
	primary key(id)
);

create table if not exists player_vars(
	id int not null auto_increment,
	player_id int not null,
	mother_base_data json,
	primary key(id),
	foreign key(player_id) references players(id) on delete cascade
);
