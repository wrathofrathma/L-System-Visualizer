from glm import mat4, vec3, vec4, normalize, inverse

def getMouseRaycast(mouse_pos, projection, view):
    # Convert to clip space
    clipped_dir = vec4(mouse_pos[0], mouse_pos[1], -1, 1)

    # Convert to eye space
    invert_proj = inverse(projection)
    eye_trans = invert_proj * clipped_dir
    eye_coords = vec4(eye_trans.x, eye_trans.y, -1, 0)

    # Convert to world space with inverse view and transforming by our eye coordinates
    inverse_view = inverse(view)
    ray_direction = inverse_view * eye_coords

    # Normalize the ray so we have a unit vector
    ray_direction = normalize(ray_direction)
    return vec3(ray_direction.x, ray_direction.y, ray_direction.z)
