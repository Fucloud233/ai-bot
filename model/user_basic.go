package model

import (
	"gorm.io/gorm"
)

type UserBasic struct {
	gorm.Model
	Phone    string
	Password string
}

// var DB *gorm.DB

func (table *UserBasic) TableName() string {
	return "user_basic"
}

func CreateUser(user *UserBasic) error {
	migrator := DB.Migrator()
	exist := migrator.HasTable("user_basic")
	if !exist {
		migrator.AutoMigrate(&user)
	}
	return DB.Create(&user).Error
}

func FindUserByPhone(phone string) UserBasic {
	user := UserBasic{}
	DB.Where("phone = ?", phone).First(&user)
	return user
}

func (user *UserBasic) CheckExist() bool {
	var num int64 = 0
	DB.Model(&user).Where("phone = ?", user.Phone).Count(&num)
	return num > 0
}
