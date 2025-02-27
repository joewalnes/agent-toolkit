# Stripe Agent Toolkit

[![Build Status](https://github.com/stripe/agent-toolkit/actions/workflows/main.yml/badge.svg)](https://github.com/stripe/agent-toolkit/actions/workflows/main.yml)

The Stripe Agent Toolkit enables popular agent frameworks including LangChain,
CrewAI, and Vercel's AI SDK, to integrate with Stripe APIs through function calling. The
library is not exhaustive of the entire Stripe API. It includes support for both Python and TypeScript and is built directly on top of the Stripe [Python][python-sdk] and [Node][node-sdk] SDKs.

Included below are basic instructions, but refer to the [Python](/python) and [TypeScript](/typescript) packages for more information.

## Python

### Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package run:

```sh
pip install stripe-agent-toolkit
```

#### Requirements

- Python 3.11+

### Usage

The library needs to be configured with your account's secret key which is
available in your [Stripe Dashboard][api-keys].

```python
from stripe_agent_toolkit.crewai.toolkit import StripeAgentToolkit

stripe_agent_toolkit = StripeAgentToolkit(
    secret_key="sk_test_...",
    configuration={
        "actions": {
            "payment_links": {
                "create": True,
            },
        }
    },
)
```

The toolkit works with LangChain and CrewAI and can be passed as a list of tools. For example:

```python
from crewai import Agent

stripe_agent = Agent(
    role="Stripe Agent",
    goal="Integrate with Stripe",
    backstory="You are an expert at integrating with Stripe",
    tools=[*stripe_agent_toolkit.get_tools()]
)
```

Examples for LangChain and CrewAI are included in [/examples](/python/examples).

## TypeScript

### Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package run:

```
npm install @stripe/agent-toolkit
```

#### Requirements

- Node 18+

### Usage

The library needs to be configured with your account's secret key which is available in your [Stripe Dashboard][api-keys]. Additionally, `configuration` enables you to specify the types of actions that can be taken using the toolkit.

```typescript
import {StripeAgentToolkit} from "@stripe/agent-toolkit/langchain";

const stripeAgentToolkit = new StripeAgentToolkit({
  secretKey: process.env.STRIPE_SECRET_KEY!,
  configuration: {
    actions: {
      paymentLinks: {
        create: true,
      },
    },
  },
});
```

#### Tools

The toolkit works with LangChain and Vercel's AI SDK and can be passed as a list of tools. For example:

```typescript
import {AgentExecutor, createStructuredChatAgent} from 'langchain/agents';

const tools = stripeAgentToolkit.getTools();

const agent = await createStructuredChatAgent({
  llm,
  tools,
  prompt,
});

const agentExecutor = new AgentExecutor({
  agent,
  tools,
});
```

#### Metered billing

For Vercel's AI SDK, you can use middleware to submit billing events for usage. All that is required is the customer ID and the input/output meters to bill.

```typescript
import {StripeAgentToolkit} from '@stripe/agent-toolkit/ai-sdk';
import {openai} from '@ai-sdk/openai';
import {
  generateText,
  experimental_wrapLanguageModel as wrapLanguageModel,
} from 'ai';

const stripeAgentToolkit = new StripeAgentToolkit({
  secretKey: process.env.STRIPE_SECRET_KEY!,
  configuration: {
    actions: {
      paymentLinks: {
        create: true,
      },
    },
  },
});

const model = wrapLanguageModel({
  model: openai('gpt-4o'),
  middleware: stripeAgentToolkit.middleware({
    billing: {
      customer: 'cus_123',
      meters: {
        input: 'input_tokens',
        output: 'output_tokens',
      },
    },
  }),
});
```

[python-sdk]: https://github.com/stripe/stripe-python
[node-sdk]: https://github.com/stripe/stripe-node
[api-keys]: https://dashboard.stripe.com/account/apikeys

