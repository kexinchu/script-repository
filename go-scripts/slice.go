package goscripts

func SliceIsEqualString(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if b[i] != v {
			return false
		}
	}
	return true
}

func SliceIsEqualStringString(a, b [][]string) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if len(v) != len(b[i]) {
			return false
		}
		for j, w := range v {
			if w != b[i][j] {
				return false
			}
		}
	}
	return true
}
