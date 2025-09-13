from vector import Vec2, Vec3, Vec4
import copy

class Mat2:
    m00: float; m01: float
    m10: float; m11: float
    
    def identity(self) -> 'Mat2':
        self.m00 = 1.0; self.m01 = 0.0
        self.m10 = 0.0; self.m11 = 1.0
        return self
    
    def __init__(self) -> None:
        self.identity()
        
    @classmethod
    def from_list(cls, m1: Vec2, m2: Vec2) -> 'Mat2':
        mat = cls()
        
        mat.m00 = m1.x; mat.m01 = m1.y
        mat.m10 = m2.x; mat.m11 = m2.y
        
        return mat
    
    def __str__(self) -> str:
        return f"[{self.m00:.2f}, {self.m01:.2f}]\n[{self.m10:.2f}, {self.m11:.2f}]"
    
    def __len__(self) -> int:
        return 2
    
    def __add__(self, other: 'Mat2') -> 'Mat2':
        copy_matrix: Mat2 = copy.copy(self)
        
        return Mat2.from_list(
            Vec2.from_values(copy_matrix.m00 + other.m00, copy_matrix.m01 + other.m01),
            Vec2.from_values(copy_matrix.m10 + other.m10, copy_matrix.m11 + other.m11)
        )
        
    def __sub__(self, other: 'Mat2') -> 'Mat2':
        copy_matrix: Mat2 = copy.copy(self)
        
        return Mat2.from_list(
            Vec2.from_values(copy_matrix.m00 - other.m00, copy_matrix.m01 - other.m01),
            Vec2.from_values(copy_matrix.m10 - other.m10, copy_matrix.m11 - other.m11)    
        )
    
    def __mul__(self, scalar: float) -> 'Mat2':
        copy_matrix: Mat2 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec2.from_values(copy_matrix.m00 * scalar, copy_matrix.m01 * scalar),
            Vec2.from_values(copy_matrix.m10 * scalar, copy_matrix.m11 * scalar)    
        )
    
    def __truediv__(self, scalar: float) -> 'Mat2':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        copy_matrix: Mat2 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec2.from_values(copy_matrix.m00 / scalar, copy_matrix.m01 / scalar),
            Vec2.from_values(copy_matrix.m10 / scalar, copy_matrix.m11 / scalar)    
        )
    
    def copy(self) -> 'Mat2':
        return copy.copy(self)
    
    def multiply_vec2(self, vec: Vec2) -> Vec2:
        return Vec2.from_values(
            self.m00 * vec.x + self.m01 * vec.y,
            self.m10 * vec.x + self.m11 * vec.y
        )
    
    def multiply_mat2(self, other: 'Mat2') -> 'Mat2':
        return Mat2.from_list(
            Vec2.from_values(
                self.m00 * other.m00 + self.m01 * other.m10,
                self.m00 * other.m01 + self.m01 * other.m11
            ),
            Vec2.from_values(
                self.m10 * other.m00 + self.m11 * other.m10,
                self.m10 * other.m01 + self.m11 * other.m11
            )
        )
    
    def transpose(self) -> 'Mat2':
        copy_matrix: Mat2 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec2.from_values(copy_matrix.m00, copy_matrix.m10),
            Vec2.from_values(copy_matrix.m01, copy_matrix.m11)
        )
    
    def matrix_float(self) -> list[list[float]]:
        return [[float(self.m00), float(self.m01)],
                [float(self.m10), float(self.m11)]]
        


class Mat3:
    m00: float; m01: float; m02: float
    m10: float; m11: float; m12: float
    m20: float; m21: float; m22: float
    
    def identity(self) -> 'Mat3':
        self.m00 = 1.0; self.m01 = 0.0; self.m02 = 0.0
        self.m10 = 0.0; self.m11 = 1.0; self.m12 = 0.0
        self.m20 = 0.0; self.m21 = 0.0; self.m22 = 1.0
        return self
    
    def __init__(self) -> None:
        self.identity()
        
    @classmethod
    def from_list(cls, m1: Vec3, m2: Vec3, m3: Vec3) -> 'Mat3':
        mat = cls()
        
        mat.m00 = m1.x; mat.m01 = m1.y; mat.m02 = m1.z
        mat.m10 = m2.x; mat.m11 = m2.y; mat.m12 = m2.z
        mat.m20 = m3.x; mat.m21 = m3.y; mat.m22 = m3.z
        
        return mat
    
    def __str__(self) -> str:
        return f"[{self.m00:.2f}, {self.m01:.2f}, {self.m02:.2f}]\n[{self.m10:.2f}, {self.m11:.2f}, {self.m12:.2f}]\n[{self.m20:.2f}, {self.m21:.2f}, {self.m22:.2f}]"
    
    def __len__(self) -> int:
        return 3
    
    def __add__(self, other: 'Mat3') -> 'Mat3':
        copy_matrix: Mat3 = copy.copy(self)
        
        return Mat3.from_list(
            Vec3.from_values(copy_matrix.m00 + other.m00, copy_matrix.m01 + other.m01, copy_matrix.m02 + other.m02),
            Vec3.from_values(copy_matrix.m10 + other.m10, copy_matrix.m11 + other.m11, copy_matrix.m12 + other.m12),
            Vec3.from_values(copy_matrix.m20 + other.m20, copy_matrix.m21 + other.m21, copy_matrix.m22 + other.m22)
        )
    
    def __sub__(self, other: 'Mat3') -> 'Mat3':
        copy_matrix: Mat3 = copy.copy(self)
        
        return Mat3.from_list(
            Vec3.from_values(copy_matrix.m00 - other.m00, copy_matrix.m01 - other.m01, copy_matrix.m02 - other.m02),
            Vec3.from_values(copy_matrix.m10 - other.m10, copy_matrix.m11 - other.m11, copy_matrix.m12 - other.m12),
            Vec3.from_values(copy_matrix.m20 - other.m20, copy_matrix.m21 - other.m21, copy_matrix.m22 - other.m22)    
        )
    
    def __mul__(self, scalar: float) -> 'Mat3':
        copy_matrix: Mat3 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec3.from_values(copy_matrix.m00 * scalar, copy_matrix.m01 * scalar, copy_matrix.m02 * scalar),
            Vec3.from_values(copy_matrix.m10 * scalar, copy_matrix.m11 * scalar, copy_matrix.m12 * scalar),
            Vec3.from_values(copy_matrix.m20 * scalar, copy_matrix.m21 * scalar, copy_matrix.m22 * scalar)    
        )
    
    def __truediv__(self, scalar: float) -> 'Mat3':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        copy_matrix: Mat3 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec3.from_values(copy_matrix.m00 / scalar, copy_matrix.m01 / scalar, copy_matrix.m02 / scalar),
            Vec3.from_values(copy_matrix.m10 / scalar, copy_matrix.m11 / scalar, copy_matrix.m12 / scalar),
            Vec3.from_values(copy_matrix.m20 / scalar, copy_matrix.m21 / scalar, copy_matrix.m22 / scalar)    
        )
    
    def copy(self) -> 'Mat3':
        return copy.copy(self)
    
    def multiply_vec3(self, vec: Vec3) -> Vec3:
        return Vec3.from_values(
            self.m00 * vec.x + self.m01 * vec.y + self.m02 * vec.z,
            self.m10 * vec.x + self.m11 * vec.y + self.m12 * vec.z,
            self.m20 * vec.x + self.m21 * vec.y + self.m22 * vec.z
        )
    
    def multiply_mat3(self, other: 'Mat3') -> 'Mat3':
        return Mat3.from_list(
            Vec3.from_values(
                self.m00 * other.m00 + self.m01 * other.m10 + self.m02 * other.m20,
                self.m00 * other.m01 + self.m01 * other.m11 + self.m02 * other.m21,
                self.m00 * other.m02 + self.m01 * other.m12 + self.m02 * other.m22
            ),
            Vec3.from_values(
                self.m10 * other.m00 + self.m11 * other.m10 + self.m12 * other.m20,
                self.m10 * other.m01 + self.m11 * other.m11 + self.m12 * other.m21,
                self.m10 * other.m02 + self.m11 * other.m12 + self.m12 * other.m22
            ),
            Vec3.from_values(
                self.m20 * other.m00 + self.m21 * other.m10 + self.m22 * other.m20,
                self.m20 * other.m01 + self.m21 * other.m11 + self.m22 * other.m21,
                self.m20 * other.m02 + self.m21 * other.m12 + self.m22 * other.m22
            )
        )
    
    def transpose(self) -> 'Mat3':
        copy_matrix: Mat3 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec3.from_values(copy_matrix.m00, copy_matrix.m10, copy_matrix.m20),
            Vec3.from_values(copy_matrix.m01, copy_matrix.m11, copy_matrix.m21),
            Vec3.from_values(copy_matrix.m02, copy_matrix.m12, copy_matrix.m22)
        )
    
    def matrix_float(self) -> list[list[float]]:
        return [[float(self.m00), float(self.m01), float(self.m02)],
                [float(self.m10), float(self.m11), float(self.m12)],
                [float(self.m20), float(self.m21), float(self.m22)]]
        


class Mat4:
    m00: float; m01: float; m02: float; m03: float
    m10: float; m11: float; m12: float; m13: float
    m20: float; m21: float; m22: float; m23: float
    m30: float; m31: float; m32: float; m33: float
    
    def identity(self) -> 'Mat4':
        self.m00 = 1.0; self.m01 = 0.0; self.m02 = 0.0; self.m03 = 0.0
        self.m10 = 0.0; self.m11 = 1.0; self.m12 = 0.0; self.m13 = 0.0
        self.m20 = 0.0; self.m21 = 0.0; self.m22 = 1.0; self.m23 = 0.0
        self.m30 = 0.0; self.m31 = 0.0; self.m32 = 0.0; self.m33 = 1.0
        return self
    
    def __init__(self) -> None:
        self.identity()
        
    @classmethod
    def from_list(cls, m1: Vec4, m2: Vec4, m3: Vec4, m4: Vec4) -> 'Mat4':
        mat = cls()
        
        mat.m00 = m1.x; mat.m01 = m1.y; mat.m02 = m1.z; mat.m03 = m1.w
        mat.m10 = m2.x; mat.m11 = m2.y; mat.m12 = m2.z; mat.m13 = m2.w
        mat.m20 = m3.x; mat.m21 = m3.y; mat.m22 = m3.z; mat.m23 = m3.w
        mat.m30 = m4.x; mat.m31 = m4.y; mat.m32 = m4.z; mat.m33 = m4.w
        
        return mat
    
    def __str__(self) -> str:
        return f"[{self.m00:.2f}, {self.m01:.2f}, {self.m02:.2f}, {self.m03:.2f}]\n[{self.m10:.2f}, {self.m11:.2f}, {self.m12:.2f}, {self.m13:.2f}]\n[{self.m20:.2f}, {self.m21:.2f}, {self.m22:.2f}, {self.m23:.2f}]\n[{self.m30:.2f}, {self.m31:.2f}, {self.m32:.2f}, {self.m33:.2f}]"
    
    def __len__(self) -> int:
        return 4
    
    def __add__(self, other: 'Mat4') -> 'Mat4':
        copy_matrix: Mat4 = copy.copy(self)
        
        return Mat4.from_list(
            Vec4.from_values(copy_matrix.m00 + other.m00, copy_matrix.m01 + other.m01, copy_matrix.m02 + other.m02, copy_matrix.m03 + other.m03),
            Vec4.from_values(copy_matrix.m10 + other.m10, copy_matrix.m11 + other.m11, copy_matrix.m12 + other.m12, copy_matrix.m13 + other.m13),
            Vec4.from_values(copy_matrix.m20 + other.m20, copy_matrix.m21 + other.m21, copy_matrix.m22 + other.m22, copy_matrix.m23 + other.m23),
            Vec4.from_values(copy_matrix.m30 + other.m30, copy_matrix.m31 + other.m31, copy_matrix.m32 + other.m32, copy_matrix.m33 + other.m33)
        )
    
    def __sub__(self, other: 'Mat4') -> 'Mat4':
        copy_matrix: Mat4 = copy.copy(self)
        
        return Mat4.from_list(
            Vec4.from_values(copy_matrix.m00 - other.m00, copy_matrix.m01 - other.m01, copy_matrix.m02 - other.m02, copy_matrix.m03 - other.m03),
            Vec4.from_values(copy_matrix.m10 - other.m10, copy_matrix.m11 - other.m11, copy_matrix.m12 - other.m12, copy_matrix.m13 - other.m13),
            Vec4.from_values(copy_matrix.m20 - other.m20, copy_matrix.m21 - other.m21, copy_matrix.m22 - other.m22, copy_matrix.m23 - other.m23),
            Vec4.from_values(copy_matrix.m30 - other.m30, copy_matrix.m31 - other.m31, copy_matrix.m32 - other.m32, copy_matrix.m33 - other.m33)    
        )
    
    def __mul__(self, scalar: float) -> 'Mat4':
        copy_matrix: Mat4 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec4.from_values(copy_matrix.m00 * scalar, copy_matrix.m01 * scalar, copy_matrix.m02 * scalar, copy_matrix.m03 * scalar),
            Vec4.from_values(copy_matrix.m10 * scalar, copy_matrix.m11 * scalar, copy_matrix.m12 * scalar, copy_matrix.m13 * scalar),
            Vec4.from_values(copy_matrix.m20 * scalar, copy_matrix.m21 * scalar, copy_matrix.m22 * scalar, copy_matrix.m23 * scalar),
            Vec4.from_values(copy_matrix.m30 * scalar, copy_matrix.m31 * scalar, copy_matrix.m32 * scalar, copy_matrix.m33 * scalar)    
        )
    
    def __truediv__(self, scalar: float) -> 'Mat4':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        copy_matrix: Mat4 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec4.from_values(copy_matrix.m00 / scalar, copy_matrix.m01 / scalar, copy_matrix.m02 / scalar, copy_matrix.m03 / scalar),
            Vec4.from_values(copy_matrix.m10 / scalar, copy_matrix.m11 / scalar, copy_matrix.m12 / scalar, copy_matrix.m13 / scalar),
            Vec4.from_values(copy_matrix.m20 / scalar, copy_matrix.m21 / scalar, copy_matrix.m22 / scalar, copy_matrix.m23 / scalar),
            Vec4.from_values(copy_matrix.m30 / scalar, copy_matrix.m31 / scalar, copy_matrix.m32 / scalar, copy_matrix.m33 / scalar)    
        )
    
    def copy(self) -> 'Mat4':
        return copy.copy(self)
    
    def multiply_vec4(self, vec: Vec4) -> Vec4:
        return Vec4.from_values(
            self.m00 * vec.x + self.m01 * vec.y + self.m02 * vec.z + self.m03 * vec.w,
            self.m10 * vec.x + self.m11 * vec.y + self.m12 * vec.z + self.m13 * vec.w,
            self.m20 * vec.x + self.m21 * vec.y + self.m22 * vec.z + self.m23 * vec.w,
            self.m30 * vec.x + self.m31 * vec.y + self.m32 * vec.z + self.m33 * vec.w
        )
    
    def multiply_mat4(self, other: 'Mat4') -> 'Mat4':
        return Mat4.from_list(
            Vec4.from_values(
                self.m00 * other.m00 + self.m01 * other.m10 + self.m02 * other.m20 + self.m03 * other.m30,
                self.m00 * other.m01 + self.m01 * other.m11 + self.m02 * other.m21 + self.m03 * other.m31,
                self.m00 * other.m02 + self.m01 * other.m12 + self.m02 * other.m22 + self.m03 * other.m32,
                self.m00 * other.m03 + self.m01 * other.m13 + self.m02 * other.m23 + self.m03 * other.m33
            ),
            Vec4.from_values(
                self.m10 * other.m00 + self.m11 * other.m10 + self.m12 * other.m20 + self.m13 * other.m30,
                self.m10 * other.m01 + self.m11 * other.m11 + self.m12 * other.m21 + self.m13 * other.m31,
                self.m10 * other.m02 + self.m11 * other.m12 + self.m12 * other.m22 + self.m13 * other.m32,
                self.m10 * other.m03 + self.m11 * other.m13 + self.m12 * other.m23 + self.m13 * other.m33
            ),
            Vec4.from_values(
                self.m20 * other.m00 + self.m21 * other.m10 + self.m22 * other.m20 + self.m23 * other.m30,
                self.m20 * other.m01 + self.m21 * other.m11 + self.m22 * other.m21 + self.m23 * other.m31,
                self.m20 * other.m02 + self.m21 * other.m12 + self.m22 * other.m22 + self.m23 * other.m32,
                self.m20 * other.m03 + self.m21 * other.m13 + self.m22 * other.m23 + self.m23 * other.m33
            ),
            Vec4.from_values(
                self.m30 * other.m00 + self.m31 * other.m10 + self.m32 * other.m20 + self.m33 * other.m30,
                self.m30 * other.m01 + self.m31 * other.m11 + self.m32 * other.m21 + self.m33 * other.m31,
                self.m30 * other.m02 + self.m31 * other.m12 + self.m32 * other.m22 + self.m33 * other.m32,
                self.m30 * other.m03 + self.m31 * other.m13 + self.m32 * other.m23 + self.m33 * other.m33
            )
        )

    def transpose(self) -> 'Mat4':
        copy_matrix: Mat4 = copy.copy(self)
        
        return copy_matrix.from_list(
            Vec4.from_values(copy_matrix.m00, copy_matrix.m10, copy_matrix.m20, copy_matrix.m30),
            Vec4.from_values(copy_matrix.m01, copy_matrix.m11, copy_matrix.m21, copy_matrix.m31),
            Vec4.from_values(copy_matrix.m02, copy_matrix.m12, copy_matrix.m22, copy_matrix.m32),
            Vec4.from_values(copy_matrix.m03, copy_matrix.m13, copy_matrix.m23, copy_matrix.m33)
        )
    
    def matrix_float(self) -> list[list[float]]:
        return [[float(self.m00), float(self.m01), float(self.m02), float(self.m03)],
                [float(self.m10), float(self.m11), float(self.m12), float(self.m13)],
                [float(self.m20), float(self.m21), float(self.m22), float(self.m23)],
                [float(self.m30), float(self.m31), float(self.m32), float(self.m33)]]
