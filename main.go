package main

import (
	"example.com/m/v2/router"
	"example.com/m/v2/utils"
)

func main() {
	utils.InitConfig()
	utils.InitMySQL()
	r := router.Router()

	r.Run(":6062")
}
