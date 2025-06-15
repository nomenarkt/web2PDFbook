from __future__ import annotations

from ..entity.renderer import Renderer, RendererError, validate_params


async def render_to_pdf(
    url: str,
    output_path: str,
    timeout: int,
    *,
    renderer: Renderer,
) -> bool:
    """Validate inputs and delegate PDF rendering."""
    validate_params(url, output_path, timeout)
    try:
        await renderer.render(url, output_path, timeout)
    except RendererError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise RendererError(str(exc)) from exc
    return True
