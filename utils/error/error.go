package error

const (
	JSONParseError int = 1001
	ParamLose int = 1002

	UserNotFound int = 2001
	UserExist int = 2002
)

func GetErrorMessage(code int) interface{} {
	var msg string
	switch code {
	case JSONParseError: msg = "json parse error"
	case ParamLose: msg = "param lose"
	case UserExist: msg = "user exits"
	}

	return map[string]interface{}{
		"message": msg,
		"code": code,
	}
}