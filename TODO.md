# TODO: Redesign UI to Particle Style

## Breakdown of Approved Plan

### 1. Setup Canvas for Particle Background
   - [ ] Add a full-window Tkinter Canvas in setup_ui() to serve as the animated background.
   - [ ] Configure Canvas to cover the main area with dark background color (#0a0a0a).
   - [ ] Initialize particle system: Create a list of 100-150 particles with random initial positions, velocities, and colors (blue to purple gradient).

### 2. Implement Particle Animation
   - [ ] Define particle properties: position (x,y), velocity (vx,vy), size, color, and attraction to center.
   - [ ] Create an update_particles() method to move particles towards a central blob point with wave-like randomness.
   - [ ] Use root.after(50, update_particles) for smooth 20fps animation loop.
   - [ ] Draw particles as semi-transparent circles/ovals on Canvas using create_oval().

### 3. Add Splash Screen Elements
   - [ ] Place "AI Assistant" title label centered above the particle blob using place() or pack() with absolute positioning.
   - [ ] Style title with large font (e.g., 32pt, bold, white/cyan glow via multiple shadowed labels if possible).
   - [ ] Add "Try Now" button below the blob, styled with cyan bg (#00ffff), rounded relief, and command to show_chat_interface().
   - [ ] Initially hide existing UI components (status, chat, input, buttons) by not packing them or using pack_forget().

### 4. Integrate with Existing UI
   - [ ] Create show_chat_interface() method: Pack/show hidden components, optionally fade out splash or keep Canvas running in background.
   - [ ] Update animate_title() to sync with particle colors or add glow effect.
   - [ ] Ensure all core functionality (send_text_message, toggle_listening, etc.) remains unchanged and accessible after splash.

### 5. Optimization and Testing
   - [ ] Test animation performance: Reduce particle count if laggy; ensure non-blocking.
   - [ ] Verify layout responsiveness on window resize.
   - [ ] Run the app to confirm particles form a central wavy blob, button triggers chat, and voice features work.
   - [ ] Update TODO.md after each major step completion.

Next Step: Start with Step 1 - Edit ui.py to add Canvas and initialize particles.
