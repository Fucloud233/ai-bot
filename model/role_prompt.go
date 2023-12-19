package model


type RolePrompt struct {
	Phone string
	BotRole string
	RolePrompt string
}	

const (
    Parent string = "parent"
    Bestie string = "bestie"
    Friend string = "friend"
    Doctor string = "doctor"
)

func GetRoleName(role string) string {
	switch role {
	case "parent": return "父母"
	case "bestie": return "闺蜜"
	case "friend": return "朋友"
	case "doctor": return "心理医生"
	default: return "解压小助手"
	}
}

var ROLES = []string{
	Parent, Bestie, Friend, Doctor,
}


func (table *RolePrompt) TableName() string {
	return "role_prompt"
}

func InitRoles(phone string) error {
	roles := []RolePrompt{}

	for _, role := range ROLES {
		bot_role := RolePrompt {
			Phone: phone,
			BotRole: role,
		}
		roles = append(roles, bot_role)
	}

	return DB.Create(&roles).Error
}


func (role *RolePrompt) UpdateRolePrompt() error {
	return DB.Model(&role).Where("phone = ? and bot_role = ?", role.Phone, role.BotRole).Update("role_prompt", role.RolePrompt).Error	
}

func GetRolePrompt(phone string, botRole string) (string, error) {
	var rolePrompt RolePrompt
	err := DB.Where("phone = ? and bot_role = ?", phone, botRole).Select("role_prompt").First(&rolePrompt).Error
	return rolePrompt.RolePrompt, err
}
