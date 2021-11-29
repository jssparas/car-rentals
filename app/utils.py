def errors_to_desc(errors):
    msg = []

    for k in errors:
        if isinstance(errors[k][0], str):
            msg.append('\"{}\": {}'.format(k, ';'.join(errors[k])))
        else:
            inner_message = ''
            for inner_errors in errors[k]:
                inner_message += errors_to_desc(inner_errors)
            msg.append('\"{}\": {}'.format(k, inner_message))

    return '. '.join(msg)