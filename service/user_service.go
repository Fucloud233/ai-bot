package service

import (
	"ai-bot/model"
	"github.com/gin-gonic/gin"
	"net/http"
)

// func CreateUser(c *gin.Context) {
// 	user := model.UserBasic{}
// 	user.Phone = c.Query("phone")
// 	user.Password = c.Query("password")
// 	err := model.CreateUser(&user)
// 	if err != nil {
// 		c.JSON(http.StatusInternalServerError, gin.H{})
// 	} else {
// 		c.JSON(http.StatusOK, gin.H{})
// 	}
// }

func CreateUser(c *gin.Context) {
	var user model.UserBasic
	err := c.ShouldBindJSON(&user)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{})
		return
	}

	if model.CheckUserExist(user.Phone) {
		c.JSON(http.StatusBadRequest, "user has existed")
		return
	}

	err1 := model.CreateUser(&user)
	err2 := model.InitRoles(user.Phone)

	status := http.StatusOK
	if err1 != nil && err2 != nil {
		status = http.StatusInternalServerError
	}

	c.JSON(status, "")
}

func Login(c *gin.Context) {
	user := model.UserBasic{}
	phone := c.PostForm("phone")
	password := c.PostForm("phone")
	findUser := model.FindUserByPhone(phone)
	if findUser.Phone != "" {
		if password == findUser.Password {
			c.JSON(http.StatusOK, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{
				"message": "密码错误",
			})
			return
		}
	} else {
		user.Phone = phone
		user.Password = password
		err := model.CreateUser(&user)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{})
		}
	}
}
