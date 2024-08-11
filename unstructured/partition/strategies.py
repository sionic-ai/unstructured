from typing import List, Optional

from unstructured.logger import logger
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.utils import dependency_exists


def validate_strategy(strategy: str, is_image: bool = False):
    """Determines if the strategy is valid for the specified filetype."""

    valid_strategies = [
        PartitionStrategy.AUTO,
        PartitionStrategy.FAST,
        PartitionStrategy.OCR_ONLY,
        PartitionStrategy.HI_RES,
    ]
    if strategy not in valid_strategies:
        raise ValueError(f"{strategy} is not a valid strategy.")

    if strategy == PartitionStrategy.FAST and is_image:
        raise ValueError("The fast strategy is not available for image files.")


def determine_pdf_or_image_strategy(
    strategy: str,
    is_image: bool = False,
    pdf_text_extractable: bool = False,
    infer_table_structure: bool = False,
    extract_images_in_pdf: bool = False,
    extract_image_block_types: Optional[List[str]] = None,
):
    """Determines what strategy to use for processing PDFs or images, accounting for fallback
    logic if some dependencies are not available."""
    return PartitionStrategy.FAST


def _determine_image_auto_strategy():
    """If "auto" is passed in as the strategy, determines what strategy to use
    for images."""
    # Use hi_res as the only default since images are only about one page
    return PartitionStrategy.HI_RES


def _determine_pdf_auto_strategy(
    pdf_text_extractable: bool = False,
    infer_table_structure: bool = False,
    extract_element: bool = False,
):
    """If "auto" is passed in as the strategy, determines what strategy to use
    for PDFs."""
    # NOTE(robinson) - Currently "hi_res" is the only strategy where
    # infer_table_structure and extract_images_in_pdf are used.
    if infer_table_structure or extract_element:
        return PartitionStrategy.HI_RES

    if pdf_text_extractable:
        return PartitionStrategy.FAST
    else:
        return PartitionStrategy.OCR_ONLY
