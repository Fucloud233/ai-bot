package utils

import (
	"fmt"

	"github.com/spf13/viper"
)

type MySQLConfig struct {
	User string
	Password string
	Host string
	Port string
	Database string
}

func (c MySQLConfig) ToDNS() string {
	return fmt.Sprintf(
		"%v:%v@tcp(%v:%v)/%v?charset=utf8mb4&parseTime=True&loc=Local",
		c.User, c.Password, c.Host, c.Port, c.Database,
	)
}

var DatabaseConfig = MySQLConfig{}

func InitConfig() {
	// read config from file
	viper.SetConfigName("aibot")
	viper.AddConfigPath("config")

	err := viper.ReadInConfig()
	if err != nil {
		fmt.Println(err)
	}

	// save the config info into MysqlConfig
	DatabaseConfig = MySQLConfig{
		User: viper.GetString("mysql.user"),
		Password: viper.GetString("mysql.password"),
		Host: viper.GetString("mysql.host"),
		Port: viper.GetString("mysql.port"),
		Database: viper.GetString("mysql.database"),
	}

	fmt.Println("aibot config inited.")
}