package goscripts

import (
	"strings"
)

// MergeMapStringInterface 合并数组值
func MergeMapStringInterface(original, added map[string]interface{}) {
	for key, value := range added {
		original[key] = value
	}
}

//GetMapStringInterface 用来获取层级很深的数组值
func GetMapStringInterface(data interface{}, path string) (interface{}, bool) {
	pathLevel := strings.Split(path, ".")
	for _, level := range pathLevel {
		if array, ok := data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				return nil, false
			}
		} else {
			return nil, false
		}

	}
	return data, true
}

//SetMapStringInterface 用来设置层级很深的数组值
func SetMapStringInterface(data interface{}, path string, new interface{}) {
	pathLevel := strings.Split(path, ".")
	var array map[string]interface{}
	var ok bool
	var key string
	for _, level := range pathLevel {
		key = level
		if array, ok = data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				//新增key
			}
		} else {
			return
		}
	}
	array[key] = new
	return
}

//DelMapStringInterface 删除层级很深的数组值
func DelMapStringInterface(data interface{}, path string) {
	pathLevel := strings.Split(path, ".")
	var array map[string]interface{}
	var ok bool
	var key string
	for _, level := range pathLevel {
		key = level
		if array, ok = data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				return
			}
		} else {
			return
		}
	}
	delete(array, key)
	return
}

//现在用的go版本小于1.18 不能用泛型，所以只能多写几个
func GetMapStringInterfaceString(data interface{}, path string) (string, bool) {
	pathLevel := strings.Split(path, ".")
	for _, level := range pathLevel {
		if array, ok := data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				return "", false
			}
		} else {
			return "", false
		}

	}
	if t, ok := data.(string); ok {
		return t, ok
	}
	return "", false
}
func GetMapStringInterfaceStringSingle(data map[string]interface{}, key string) (string, bool) {
	var v interface{}
	if value, exist := data[key]; exist {
		v = value
	} else {
		return "", false
	}

	if t, ok := v.(string); ok {
		return t, ok
	}
	return "", false
}
func GetMapStringInterfaceSlice(data map[string]interface{}, key string) ([]interface{}, bool) {
	var v interface{}
	if value, exist := data[key]; exist {
		v = value
	} else {
		return nil, false
	}

	if t, ok := v.([]interface{}); ok {
		return t, ok
	}
	return nil, false
}

func GetMapStringInterfaceInt32(data interface{}, path string) (int32, bool) {
	pathLevel := strings.Split(path, ".")
	for _, level := range pathLevel {
		if array, ok := data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				return 0, false
			}
		} else {
			return 0, false
		}

	}
	if t, ok := data.(int32); ok {
		return t, ok
	}
	return 0, false
}
func GetMapStringInterfaceInt32Single(data map[string]interface{}, path string) (int32, bool) {
	if value, exist := data[path]; exist {
		if t, ok := value.(int32); ok {
			return t, ok
		}
	}
	return 0, false
}

func GetMapStringInterfaceFloat(data interface{}, path string) (float64, bool) {
	pathLevel := strings.Split(path, ".")
	for _, level := range pathLevel {
		if array, ok := data.(map[string]interface{}); ok {
			if value, exist := array[level]; exist {
				data = value
			} else {
				return 0, false
			}
		} else {
			return 0, false
		}

	}
	if t, ok := data.(float64); ok {
		return t, ok
	}
	return 0, false
}

func InArrayInt32(val int32, array []int32) bool {
	for _, v := range array {
		if v == val {
			return true
		}
	}
	return false
}
func InArrayString(val string, array []string) bool {
	for _, v := range array {
		if v == val {
			return true
		}
	}
	return false
}

func InArray(val interface{}, array []interface{}) bool {
	for _, v := range array {
		if v == val {
			return true
		}
	}
	return false
}

func CopyMapStringInterface(src map[string]interface{}) map[string]interface{} {
	if src == nil {
		return nil
	}
	newMap := make(map[string]interface{}, len(src))
	for k, v := range src {
		newMap[k] = v
	}
	return newMap
}

//二位数组赋值
func AddMapMap(m map[string]interface{}, k, key, val string) {
	var res map[string]string
	if m[k] == nil {
		res = make(map[string]string)
	} else {
		res = m[k].(map[string]string)
	}
	res[key] = val
	m[k] = res
}
