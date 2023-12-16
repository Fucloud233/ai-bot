package router

import (
	"example.com/m/v2/service"
	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	r := gin.Default()
	r.GET("index/login", service.Login)
	r.POST("user", service.CreateUser)
	return r
}
