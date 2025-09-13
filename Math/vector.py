from math import sqrt
import copy

class Vec2:
    x: float
    y: float
    
    def __init__(self):
        self.x:float = 0.0
        self.y:float = 0.0
        
    @classmethod
    def from_values(cls, x: float, y: float) -> 'Vec2':
        vec = cls()
        vec.x = x
        vec.y = y
        return vec
        
    def __str__(self):
        return f"[{self.x:.3f}, {self.y:.3f}]"
    
    def __len__(self) -> int:
        return 2
    
    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2.from_values(
            self.x + other.x,
            self.y + other.y
        )
    
    def __sub__(self, other: 'Vec2') -> 'Vec2':
        return Vec2.from_values(
            self.x - other.x,
            self.y - other.y
        )
    
    def __mul__(self, scalar: float) -> 'Vec2':        
        return Vec2.from_values(
            self.x * scalar,
            self.y * scalar
        )
        
    def __truediv__(self, scalar: float) -> 'Vec2':        
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        return Vec2.from_values(
            self.x / scalar,
            self.y / scalar
        )
        
    def copy(self) -> 'Vec2':
        return copy.copy(self)
    
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)
    
    def normalize(self) -> 'Vec2':
        mag = self.magnitude()
        
        if mag == 0:
            return self
        
        self.x /= mag
        self.y /= mag
        
        return self
        
    def scalar_product(self, other: 'Vec2') -> float:
        return self.x * other.x + self.y * other.y
    
    def to_float(self) -> list[float]:
        return [self.x, self.y]
    
    
    
class Vec3:
    x: float
    y: float
    z: float
    
    def __init__(self):
        self.x:float = 0.0
        self.y:float = 0.0
        self.z:float = 0.0
        
    @classmethod
    def from_values(cls, x: float, y: float, z: float) -> 'Vec3':
        vec = cls()
        vec.x = x
        vec.y = y
        vec.z = z
        return vec
    
    def __str__(self):
        return f"[{self.x:.3f}, {self.y:.3f}, {self.z:.3f}]"
    
    def copy(self) -> 'Vec3':
        return copy.copy(self)
    
    def __len__(self) -> int:
        return 3
    
    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3.from_values(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def __sub__(self, other: 'Vec3') -> 'Vec3':
        return Vec3.from_values(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
    
    def __mul__(self, scalar: float) -> 'Vec3':        
        return Vec3.from_values(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar
        )
        
    def __truediv__(self, scalar: float) -> 'Vec3':        
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        return Vec3.from_values(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar
        )
    
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> 'Vec3':
        mag = self.magnitude()
        
        if mag == 0:
            return self
        
        self.x /= mag
        self.y /= mag
        self.z /= mag
        
        return self
    
    def scalar_product(self, other: 'Vec3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def to_float(self) -> tuple[float, float, float]:
        return (float(self.x), float(self.y), float(self.z))



class Vec4:
    x: float
    y: float
    z: float
    w: float
    
    def __init__(self):
        self.x:float = 0.
        self.y:float = 0.
        self.z:float = 0.
        self.w:float = 0.
        
    @classmethod
    def from_values(cls, x: float, y: float, z: float, w: float) -> 'Vec4':
        vec = cls()
        vec.x = x
        vec.y = y
        vec.z = z
        vec.w = w
        return vec
        
    def __str__(self):
        return f"[{self.x:.3f}, {self.y:.3f}, {self.z:.3f}, {self.w:.3f}]"
    
    def __len__(self) -> int:
        return 4
    
    def copy(self) -> 'Vec4':
        return copy.copy(self)
    
    def __add__(self, other: 'Vec4') -> 'Vec4':
        return Vec4.from_values(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
        )
        
    def __sub__(self, other: 'Vec4') -> 'Vec4':
        return Vec4.from_values(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w
        )
    
    def __mul__(self, scalar: float) -> 'Vec4':        
        return Vec4.from_values(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
            self.w * scalar
        )
    
    def __truediv__(self, scalar: float) -> 'Vec4':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        
        return Vec4.from_values(
            self.x / scalar,
            self.y / scalar,
            self.z / scalar,
            self.w / scalar
        )
        
    def magnitude(self) -> float:
        mag = self.x**2 + self.y**2 + self.z**2 + self.w**2
        
        return sqrt(mag)

    def normalize(self) -> 'Vec4':
        mag = self.magnitude()
        
        if mag == 0:
            return self
        
        self.x /= mag
        self.y /= mag
        self.z /= mag
        self.w /= mag
        
        return self
    
    def scalar_product(self, other: 'Vec4') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w
    
    def to_float(self) -> list[float]:
        return [self.x, self.y, self.z, self.w]