package main

import (
	"example.com/m/v2/model"
	"example.com/m/v2/router"
	"example.com/m/v2/utils"
)

func main() {
	utils.InitConfig()
	model.InitMySQL()
	r := router.Router()

	r.Run(":6062")
}
