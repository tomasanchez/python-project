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
> > <cite>[Cosmic Python - Chapter 2](https://www.cosmicpython.com/book/chapter_02_repository.html)</cite>