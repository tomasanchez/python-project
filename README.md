# FastAPI Project Template

A Project Template based on [Cosmic Python](https://www.cosmicpython.com/) `Allocation` service example.

## Context

![Context](https://www.cosmicpython.com/book/images/apwp_0102.png)

> At a high level, we have separate systems that are responsible for buying stock, selling stock to customers, and
> shipping goods to customers. A system in the middle needs to coordinate the process by allocating stock to a
> customer’s
> orders.
>
> <cite>[Cosmic Python - Chapter 1](https://www.cosmicpython.com/book/chapter_01_domain_model.html#allocation_context_diagram)</cite>

## Architecture

### Repositories

Apply dependency inversion to your ORM
Our domain model should be free of infrastructure concerns, so your ORM should import your model, and not the other way
around.

The Repository pattern is a simple abstraction around permanent storage
The repository gives you the illusion of a collection of in-memory objects. It makes it easy to create a FakeRepository
for testing and to swap fundamental details of your infrastructure without disrupting your core application.

![Repository pattern](https://www.cosmicpython.com/book/images/apwp_0201.png)

> Are these ports and adapters? Or is it hexagonal architecture? Is that the same as onion architecture? What about the
> clean architecture? What’s a port, and what’s an adapter? Why do you people have so many words for the same thing?
>
> Ports and adapters came out of the OO world, and the definition we hold onto is that the port is the interface between
> our application and whatever it is we wish to abstract away, and the adapter is the implementation behind that
> interface
> or abstraction.
>
> Concretely, in this chapter, AbstractRepository is the port, and SqlAlchemyRepository and FakeRepository are the
> adapters.
>
> <cite>[Cosmic Python - Chapter 2](https://www.cosmicpython.com/book/chapter_02_repository.html)</cite>

### Service Layer

This pattern takes care of orchestrating workflows and defining use cases for the system. It will become the main way
into the application, as it shows what the aim is.

Even though we are working with FastAPI instead of Flask, the same applies. Just replace `Flask` with `FastAPI`

![Service Layer](https://www.cosmicpython.com/book/images/apwp_0402.png)

See
the [Service Layer Trade-offs](https://www.cosmicpython.com/book/chapter_04_service_layer.html#chapter_04_service_layer_tradeoffs)
section for more details.

> There are still some bits of awkwardness to tidy up:
>
> The service layer is still tightly coupled to the domain, because its API is expressed in terms of OrderLine objects.
> In **Chapter 5**, we’ll fix that and talk about the way that the service layer enables more productive
> TDD.
>
> The service layer is tightly coupled to a session object. In **Chapter 6**, e’ll introduce one more pattern that works
> closely with the Repository and Service Layer patterns, the Unit of Work pattern, and everything will be absolutely
> lovely. You’ll see!
>
> <cite>[Cosmic Python - Chapter 4](https://www.cosmicpython.com/book/chapter_04_service_layer.html)</cite>

As our application gets bigger, we’ll need to keep tidying our directory structure. The layout of our project gives us
useful hints about what kinds of object we’ll find in each file.

Here’s one way we could organize things:

```text
.
├── config.py
├── domain  #(1)
│   ├── __init__.py
│   └── model.py
├── service_layer #(2
│   ├── __init__.py
│   └── services.py
├── adapters  #(3)
│   ├── __init__.py
│   ├── orm.py
│   └── repository.py
├── entrypoints  (4)
│   ├── __init__.py
│   └── flask_app.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── unit
    │   ├── test_allocate.py
    │   ├── test_batches.py
    │   └── test_services.py
    ├── integration
    │   ├── test_orm.py
    │   └── test_repository.py
    └── e2e
        └── test_api.py
```

- **(1)**. Domain, from Domain Driven Architecture.
- **(2)**. The service layer will be distinguished. What is the difference between a domain service and a service layer?
    - Application service (our service layer) ts job is to handle requests from the outside world and to orchestrate an
      operation.
    - Domain Service. This is the name for a piece of logic that belongs in the domain model but doesn't sit naturally
      inside a stateful
      entity or value object. For example, if you were building a shopping cart application, you might choose to build
      taxation rules as a domain service.
- **(3)**. Adapters, it comes from ports and adapters terminology. This will fill up with any other abstractions around
  external I/O. Strictly speaking, you would call these secondary adapters or driven adapters, or sometimes
  inward-facing adapters.
- **(4)**. Entrypoints are the places we drive our application from. In the official ports and adapters terminology,
  these are adapters too, and are referred to as primary, driving, or outward-facing adapters.

#### High Gear and Low Gear

Many of our unit tests operate at a lower lever, closer to the domain model.

> I was initially skeptical of all Bob’s architectural patterns, but seeing an actual test pyramid made me a convert.
>
> Once you implement domain modeling and the service layer, you really actually can get to a stage where unit tests
> outnumber integration and end-to-end tests by an order of magnitude. Having worked in places where the E2E test build
> would take hours ("wait 'til tomorrow," essentially), I can’t tell you what a difference it makes to be able to run
> all your tests in minutes or seconds.
>
> Read on for some guidelines on how to decide what kinds of tests to write and at which level. The high gear versus low
> gear way of thinking really changed my testing life.
>
> <cite>[Cosmic Python - Chapter 5](https://www.cosmicpython.com/book/chapter_05_high_gear_low_gear.html)</cite>

Is it wrong to test against the domain model?

![The Test Spectrum](https://www.cosmicpython.com/book/images/apwp_0501.png)

A test for the HTTP API tells us nothing about the fine-grained design of our objects, because it sits at a much higher
level of abstraction. We can rewrite our entire application and, so long as we don't change the URL paths or request
format, our tests will continue to pass.

At the other end of the spectrum, in previous [chapters](https://www.cosmicpython.com/book/chapter_01_domain_model.html)
, tests helped us understand the objects we needed. Guiding us to a design that makes sense and reads in the domain
language. When starting a new project or when hitting a particularly gnarly problem, we will drop back down to writing
tests against the domain model, so we get better feedback and executable documentation of our intent.

> The metaphor we use is that of shifting gears. When starting a journey, the bicycle needs to be in a low gear so that
> it can overcome inertia. Once we’re off and running, we can go faster and more efficiently by changing into a high
> gear;
> but if we suddenly encounter a steep hill or are forced to slow down by a hazard, we again drop down to a low gear
> until
> we can pick up speed again.
>
> <cite>[Cosmic Python - Chapter 5](https://www.cosmicpython.com/book/chapter_05_high_gear_low_gear.html#_high_and_low_gear)</cite>
