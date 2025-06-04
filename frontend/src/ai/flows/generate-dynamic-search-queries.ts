'use server';

/**
 * @fileOverview This file defines a Genkit flow for generating dynamic search queries from natural language input.
 *
 * The flow takes a natural language query as input and returns a structured search query.
 * It also determines whether specific details should be included or excluded from the search.
 *
 * @module src/ai/flows/generate-dynamic-search-queries
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

/**
 * Input schema for the dynamic search query generation flow.
 */
const GenerateDynamicSearchQueriesInputSchema = z.object({
  naturalLanguageQuery: z.string().describe('The natural language query from the user.'),
});

export type GenerateDynamicSearchQueriesInput = z.infer<
  typeof GenerateDynamicSearchQueriesInputSchema
>;

/**
 * Output schema for the dynamic search query generation flow.
 */
const GenerateDynamicSearchQueriesOutputSchema = z.object({
  structuredQuery: z.string().describe('The structured search query to execute.'),
  detailsInclusionPreference: z
    .string()
    .describe(
      'Whether to include or exclude specific details from the search query.  Valid values: INCLUDE, EXCLUDE'
    ),
});

export type GenerateDynamicSearchQueriesOutput = z.infer<
  typeof GenerateDynamicSearchQueriesOutputSchema
>;

/**
 * Flow function for generating dynamic search queries.
 * @param input The input object containing the natural language query.
 * @returns A promise that resolves to the structured search query and details inclusion preference.
 */
export async function generateDynamicSearchQueries(
  input: GenerateDynamicSearchQueriesInput
): Promise<GenerateDynamicSearchQueriesOutput> {
  return generateDynamicSearchQueriesFlow(input);
}

const generateDynamicSearchQueriesPrompt = ai.definePrompt({
  name: 'generateDynamicSearchQueriesPrompt',
  input: {schema: GenerateDynamicSearchQueriesInputSchema},
  output: {schema: GenerateDynamicSearchQueriesOutputSchema},
  prompt: `You are an AI assistant designed to generate dynamic search queries from natural language input.

  Your task is to convert the given natural language query into a structured search query that can be executed against a database of products.
  You also need to determine whether the user intends to include or exclude specific details from the search.

  For example, if the user says 'Show me products under $50 with high profit margins,' you should generate a structured query that filters products based on price and profit margin.
  You should also set the detailsInclusionPreference to 'INCLUDE' to indicate that the user wants to include these specific details in the search.

  If the user says 'Show me products except for those with low supplier reliability,' you should generate a structured query that excludes products based on supplier reliability.
  You should also set the detailsInclusionPreference to 'EXCLUDE' to indicate that the user wants to exclude these specific details from the search.

  Natural Language Query: {{{naturalLanguageQuery}}}
  `,
});

const generateDynamicSearchQueriesFlow = ai.defineFlow(
  {
    name: 'generateDynamicSearchQueriesFlow',
    inputSchema: GenerateDynamicSearchQueriesInputSchema,
    outputSchema: GenerateDynamicSearchQueriesOutputSchema,
  },
  async input => {
    const {output} = await generateDynamicSearchQueriesPrompt(input);
    return output!;
  }
);
