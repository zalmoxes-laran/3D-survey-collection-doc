Inhering properties
===================

.. _inheriting_props_definition:

What is the inheriting effect ?
-------------------------------

For some actor nodes is possible to just inherit properties from other ones (following the law of the property inheriting). In different words, in several situations a property that has been already declared can simple be re-used by other actors without re-instancig it again. 

There are two different situations:

#. In the case of the material property of a marble lintel (USM100), the corresponding USV/s 101(reconstruction of the lost part of the lintel) will automatically inherit this property.

#. Other properties are not automatically inherited: in some cases the broken lintel will preserve its original height so that it can be reused by the USV/s 101, in other situations the original height property is lost and can't be reused.

Let's see in the next section how these two different situations can be managed.

The formal notation of the inheriting effect.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the first example, the relation between the two actor nodes is one of these that are normed by fixed rules (see the table). Here no formal notation is required: the properties that will pass from a node to another are assumed by the human reader or eventually by parsing algoritms following the concordance table below. 

+---+------------+-----------+-----------+ 
| n | Lower node | Upper node| Properties|
+===+============+===========+===========+ 
| 1 | US/USM     | USV/s     | - material|
|   |            |           | - tecnique|
|   |            |           | - position|
+---+------------+-----------+-----------+ 
| 2 | SF         |  VSF      | - material|
|   |            |           | - tecnique|
+---+------------+-----------+-----------+

In the second situation, the upper node (USV/s) will be connected with the USM node through a dotted line and a property node in the middle representing the name inheriting property (no descriprion is required in the description field.