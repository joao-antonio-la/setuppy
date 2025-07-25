def validate_number(self, e):
    tf = e.control
    filtered = ''.join(filter(str.isdigit, tf.value))
    if tf.value != filtered:
        tf.value = filtered
        tf.update()
