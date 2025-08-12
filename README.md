# 🎯 2D Collision Physics Simulator

A real-time physics engine built in Python that demonstrates **conservation of momentum**, **energy dynamics**, and **collision mechanics** through interactive visualization.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame
```

### Run the Simulator
```bash
python collision_2d.py
```

## 📖 What Is This?

This simulator shows you **real physics in action**! Watch colored circles bounce around, collide with each other and walls, while live charts track the underlying physics principles that govern all motion.

### 🎮 Interactive Controls

| Key | Action | Description |
|-----|--------|-------------|
| `SPACE` | Reset | Generate new random bodies |
| `P` | Pause | Pause/unpause the simulation |
| `T` | Trails | Toggle motion trails (see where bodies have been) |
| `V` | Vectors | Toggle velocity arrows (see speed & direction) |
| `C` | Charts | Toggle live physics data charts |
| `1` | Elastic | Perfect bouncy collisions (e=1.0) |
| `2` | Semi-Elastic | Slightly less bouncy (e=0.8) |
| `3` | Inelastic | Moderately bouncy (e=0.5) |
| `4` | Very Inelastic | Low bounce (e=0.2) |
| `ESC` | Exit | Close the simulator |

## 🔬 Physics Concepts Explained

### 1. Conservation of Momentum
**The Big Idea**: In a closed system, total momentum never changes.

```
Total Momentum = m₁v₁ + m₂v₂ + m₃v₃ + ...
```

**What You'll See**: The "Total Momentum" chart stays roughly flat, even during chaotic collisions!

### 2. Kinetic Energy
**The Big Idea**: Energy of motion. Unlike momentum, this *can* be lost in collisions.

```
Kinetic Energy = ½mv²
```

**What You'll See**: 
- **Elastic collisions (e=1.0)**: Energy stays constant
- **Inelastic collisions (e<1.0)**: Energy decreases over time

### 3. Coefficient of Restitution (e)
**The Big Idea**: How "bouncy" a collision is.

- **e = 1.0**: Perfectly elastic (rubber ball on hard floor)
- **e = 0.8**: Somewhat elastic (basketball bounce)
- **e = 0.5**: Moderately inelastic (tennis ball on grass)
- **e = 0.2**: Highly inelastic (clay ball collision)

### 4. Impulse-Momentum Theorem
**The Big Idea**: A quick force (impulse) changes momentum instantly.

```
Impulse = Change in Momentum = Force × Time
```

**What You'll See**: When circles collide, they instantly change direction and speed.

## 📊 Live Data Visualization

### Four Real-Time Charts

1. **🔵 Total Momentum**
   - Should stay relatively constant (conservation law!)
   - Small fluctuations are normal due to wall collisions

2. **🔴 Kinetic Energy**
   - Flat line for elastic collisions
   - Decreasing steps for inelastic collisions
   - Shows energy being "lost" (converted to heat in real life)

3. **🟢 Average Speed**
   - Overall "activity" level of the system
   - Decreases over time in inelastic systems

4. **🟠 Collisions/Frame**
   - How many impacts are happening right now
   - Spikes during high-activity moments

## 🧮 The Mathematics Behind It

### Core Collision Formula

When two circles collide, we calculate the impulse:

```
j = -(1 + e) × (relative_velocity · normal) / (1/m₁ + 1/m₂)
```

Then update velocities:
```
v₁_new = v₁_old - (j/m₁) × normal
v₂_new = v₂_old + (j/m₂) × normal
```

### Vector Operations Used

- **Distance**: `d = √[(x₂-x₁)² + (y₂-y₁)²]`
- **Normal Vector**: `n̂ = (pos₂ - pos₁) / |pos₂ - pos₁|`
- **Dot Product**: `a·b = |a||b|cos(θ)`

## 🎯 Educational Experiments

### Experiment 1: Conservation Laws
1. Press `1` (elastic) and watch both momentum and energy stay constant
2. Press `3` (inelastic) and see energy decrease while momentum stays constant

### Experiment 2: Mass Effects
- Small circles bounce dramatically off large ones
- Large circles barely react to small collisions
- Mass = radius² (like constant density disks)

### Experiment 3: Energy Dissipation
1. Start with `1` (elastic) - high energy system
2. Switch to `4` (highly inelastic) - watch energy drain away
3. Bodies eventually move very slowly

### Experiment 4: Visual Analysis
- Press `T` to see motion trails
- Press `V` to see velocity vectors
- Watch how vectors change during collisions

## 🔧 Technical Implementation

### Key Classes

- **`Body`**: Represents a physics object with position, velocity, mass, and color
- **`World`**: Manages all bodies, handles collisions, updates physics
- **`Chart`**: Real-time data visualization for physics quantities

### Physics Pipeline (60 FPS)
1. **Move**: Update positions based on velocity
2. **Wall Collisions**: Bounce off boundaries
3. **Body Collisions**: Detect overlaps and resolve
4. **Position Correction**: Prevent objects from "sinking"
5. **Data Update**: Feed charts with current physics values

### Collision Detection
- **Broad Phase**: Check all pairs of bodies
- **Narrow Phase**: Distance-based circle overlap
- **Resolution**: Impulse-based velocity updates

## 💡 Real-World Applications

### Game Development
- **Physics Engines**: Unity, Unreal Engine use similar principles
- **Particle Systems**: Explosions, debris, fluid simulation
- **Character Movement**: Bouncing, sliding, impact effects

### Education & Research
- **Interactive Learning**: Visualize abstract physics concepts
- **Scientific Simulation**: Molecular dynamics, planetary motion
- **Engineering**: Material collision analysis, safety testing

### Animation & VFX
- **Realistic Motion**: Natural-looking collisions and bounces
- **Pre-visualization**: Test physics before expensive rendering
- **Interactive Art**: Physics-based installations and games

## ⚙️ Configuration Options

Edit these values at the top of `collision_2d.py`:

```python
N_BODIES = 3              # Number of circles (recommended: 3-6)
RADIUS_RANGE = (20, 35)   # Size range of circles
SPEED_RANGE = (60, 180)   # Initial speed range
E_COEFF = 1.0             # Default elasticity
MASS_FROM_RADIUS = True   # Whether mass = radius²
```

## 🐛 Troubleshooting

### Performance Issues
- **Reduce N_BODIES**: Try 3-4 bodies instead of 6+
- **Disable Charts**: Press `C` to turn off real-time graphing
- **Lower FPS**: Change `TARGET_FPS` from 60 to 30

### Physics Looks Wrong
- **Bodies stick together**: Increase `PERCENT_CORRECTION` to 0.9
- **System gains energy**: Check that `E_COEFF` ≤ 1.0
- **Jittery motion**: Decrease `SLOP` value to 0.005

### Visual Issues
- **Circles overlap walls**: Adjust `WALL_MARGIN`
- **Charts not showing**: Press `C` or check `SHOW_CHARTS = True`
- **Arrows too small/large**: Modify `VELOCITY_VECTOR_SCALE`

## 📚 Learning Path

### Beginner (No Physics Background)
1. Run the simulator and play with controls
2. Watch the momentum chart stay flat - that's conservation!
3. Compare elastic (1) vs inelastic (4) collisions
4. Try trails (T) to see motion patterns

### Intermediate (Some Physics Knowledge)
1. Understand the impulse formula and how it conserves momentum
2. Observe energy loss in inelastic collisions
3. Experiment with mass effects (small vs large circles)
4. Study the vector math in `resolve_collision()`

### Advanced (Physics/CS Student)
1. Analyze the collision detection algorithm
2. Understand positional correction and why it's needed
3. Modify the code to add gravity or friction
4. Implement different collision shapes (rectangles, polygons)

## 🔮 Extension Ideas

### Physics Features
- **Gravity**: Add downward acceleration
- **Friction**: Gradually slow down bodies
- **Rotation**: Spinning circles with angular momentum
- **Springs**: Connect bodies with elastic forces

### Visual Enhancements
- **Particle Effects**: Sparks on collision
- **Sound**: Audio feedback for impacts
- **3D Mode**: Extend to three dimensions
- **Custom Shapes**: Rectangles, triangles, irregular polygons

### Simulation Features
- **Replay System**: Record and playback collisions
- **Stress Testing**: Gradually increase number of bodies
- **Scenario Builder**: Pre-set interesting configurations
- **Data Export**: Save physics data to CSV files

## 📄 License

MIT License - Feel free to use, modify, and distribute!

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or submit a pull request!

### Development Setup
```bash
git clone <repository-url>
cd collision-simulator
pip install pygame
python collision_2d.py
```

---

** Educational Note**: This simulator demonstrates fundamental physics principles used in everything from video games to spacecraft navigation. The same conservation laws govern billiard balls and planetary motion!

**⭐ If this helped you understand physics or game development, star the repository! 😉**
