# This is a test script for a LLM model using etalon metrics and evaluation framework 

#__________Environent Setup__________
$env:OPENAI_API_BASE="http://localhost:1234/v1" # Set the API base URL to the local LLM server
$env:OPENAI_API_KEY="lm-studio" # Set the API key to a placeholder value for testing

#__________Test Cases__________
$env:MODEL = "microsoft/phi-4-mini-reasoning"

#_____Scripts_____
python -m etalon.run_benchmark `
--client_config_model $env:MODEL `
--max_completed_requests 20 `
--timeout 1800 `
--client_config_num_clients 4 `
--client_config_num_concurrent_requests_per_client 5 `
--metrics_config_output_dir "result_outputs/$env:MODEL" `
--request_interval_generator_config_type "poisson" `
--poisson_request_interval_generator_config_qps 0.05 `
--request_length_generator_config_type "trace" `
--trace_request_length_generator_config_trace_file "./data/processed_traces/arxiv_summarization_filtered_stats_llama2_tokenizer.csv" `
--trace_request_length_generator_config_max_tokens 2048 `
--deadline_config_ttft_deadline 10.0 `
--deadline_config_tbt_deadline 0.2 `
--metrics_config_should_write_metrics