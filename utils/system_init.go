package utils

import (
	"fmt"
	"github.com/spf13/viper"
)

func InitConfig() {
	viper.SetConfigName("aibot")
	viper.AddConfigPath("config")
	err := viper.ReadInConfig()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("aibot config inited.")
}

//func InitMySQL() {
//	newLogger := logger.New(
//		log.New(os.Stdout, "\r\n", log.LstdFlags),
//		logger.Config{
//			SlowThreshold: time.Second,
//			LogLevel:      logger.Info,
//			Colorful:      true,
//		},
//	)
//	fmt.Println("连接数据库", viper.GetString("mysql.dns"))
//	model.DB, _ = gorm.Open(mysql.Open(viper.GetString("mysql.dns")),
//		&gorm.Config{Logger: newLogger})
//	fmt.Println("MySQL inited.", viper.GetString("mysql"))
//}
