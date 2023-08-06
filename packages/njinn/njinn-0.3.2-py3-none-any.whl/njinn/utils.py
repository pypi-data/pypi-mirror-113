from typing import Optional


def try_get_annotation_class(annotation, condition) -> Optional[type]:
    if hasattr(annotation, "__args__"):  # Union[] hint
        return next(
            (type_arg for type_arg in annotation.__args__ if condition(type_arg)), None,
        )
    else:
        return annotation if condition(annotation) else None
