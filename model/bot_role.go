package model


type BotRole struct {
	Phone string
	Role string
	RolePrompt string
}	

const (
    Parent string = "parent"
    Bestie string = "bestie"
    Friend string = "friend"
    Doctor string = "doctor"
)

var ROLES = []string{
	Parent, Bestie, Friend, Doctor,
}


func (table *BotRole) TableName() string {
	return "bot_role"
}

func InitRoles(phone string) error {
	roles := []BotRole{}

	for _, role := range ROLES {
		bot_role := BotRole {
			Phone: phone,
			Role: role,
		}
		roles = append(roles, bot_role)
	}

	return DB.Create(&roles).Error
}


func (role *BotRole) UpdateRolePrompt() error {
	return DB.Model(&role).Update("role_prompt", role.RolePrompt).Error	
}


