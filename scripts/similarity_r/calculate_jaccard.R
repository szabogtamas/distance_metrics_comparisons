#!/usr/bin/env Rscript

############################################################################
#                                                                          #
#   Calculates Jaccard similarity of entities with categorical labels.     #
#   Preferred input is long format data, but it is possible to adapt.      #
#                                                                          #
############################################################################

scriptDescription <- "Calculate Jaccard similarity of labelled entities."

scriptMandatoryArgs <- list(
  inFile = list(
    abbr="-i",
    help="Path to a table with input data."
  )
)

scriptOptionalArgs <- list(
  inFormat = list(
    abbr="-f",
    default="long",
    help="Format of data in the input. Possible values are [long, tabular, nested, binary]."
  ),
  outPath = list(
    abbr="-o",
    default="jaccard_similarity.csv",
    help="Path to output table capturing similarities."
  )
)

for (pk in c("tidyr", "dplyr")){
  if(!(pk %in% (.packages()))){
    library(pk, character.only=TRUE)
  }
}


#' The main function of the script, executed only if called from command line.
#' Calls subfunctions according to supplied command line arguments.
#' 
#' @param opt list. a named list of all command line options; will be passed on 
#' 
#' @return Not intended to return anything, but rather to save outputs to files.
main <- function(opt){
  
  cat("Standardizing input\n")
  main_mat <- standardize_input_data(opt$inFile, opt$inFormat)
  
  cat("Calculating similarity\n")
  jaccard_sims <- calculate_jaccard(main_mat)

  cat("Saving similarity matrix\n")
  write.csv(jaccard_sims, opt$outPath)

  invisible(NULL)
}


#' Convert input data from the accepted formats to a stadard binarized matrix.
#' 
#' @param input_path string.  Path to inpu file.
#' @param data_format string. Format of data in the input. Possible values are [long, tabular, nested, binary].
#' 
#' @return matrix.
standardize_input_data <- function(input_path, data_format){

  in_tab <- read.csv(input_path)

  if (data_format == "tabular") {
    in_tab <- in_tab %>%
        pivot_longer(everything()) %>%
        rename(Entity = name, Label = value) %>%
        dplyr::filter(!is.na(Label))
  }

  if (data_format == "nested") {
    in_tab[[2]] <- strsplit(in_tab[[2]], ";")
    colnames(in_tab <- c("Entity", "Label"))
    in_tab <- unnest(in_tab, Label)
  }

  if (data_format %in% c("long", "nested", "tabular")) {
  in_tab <- in_tab %>%
    mutate(value = 1) %>%
    pivot_wider(names_from=Label, values_fill=0) %>%
    column_to_rownames("Entity")
  } else {
    in_tab <- column_to_rownames(in_tab, "Entity")
  }

  return(in_tab)
}


#' Calculate Jaccard similarities from a stadard binarized matrix.
#' 
#' @param hot_matrix matrux.  Input in banarized (one-hot-encoded) format.
#'  
#' @return matrix.
calculate_jaccard <- function(hot_matrix){
  hot_matrix %>%
    {1 - .} %>%
    as.matrix() %>%
    data.frame() %>%
    rownames_to_column("Entity")
}


####    Intarfacing with command line below, nothing related to the main functionality    ####

if (!interactive()) {
  
  # Initialize parser with verbosity and description of script
  parser <- OptionParser(usage=paste0("%prog [options]\nDescription:\n  ", scriptDescription))
  parser <- add_option(
    parser,
    c("-v", "--verbose"),
    action="store_true",
    default=FALSE,
    help="Print some progress messages to stdout."
    )
  parser <- add_option(
    parser,
    c("-q", "--quietly"),
    action="store_false",
    dest="verbose",
    help="Create figures quietly, without printing to stdout."
  )
  
  # Add custom arguments to parser
  for (arg_def in list(scriptMandatoryArgs, scriptOptionalArgs)){
    for (arg_name in names(arg_def)){
      rg <- al[[arg_name]]
      arg_alias <- paste0("--", arg_name)
      if ("abbr" %in% names(rg) ) {
        arg_alias <- c(rg[["abbr"]], arg_alias)
        rg[["abbr"]] <- NULL
      }
      parser <- do.call(add_option, c(list(parser, arg_alias), rg))
    }
  }
  opt <- parse_args(parser)

  # Check if mandatory arguments are present
  passed_args <- opt[names(scriptMandatoryArgs)]
  if (any(is.na(names(passed_args)))) {
    if (opt$verbose) { 
      write("Sorry, cannot proceed without all mandatory arguments.\n", stderr())
    }
    checkpass <- FALSE
  } else {
    checkpass <- TRUE
  }

  # Execute main function if mandatory arguments are set (otherwise print help message)
  if (checkpass) { 
    main(opt)
  } else {
    print_help(parser)
  }
  
}