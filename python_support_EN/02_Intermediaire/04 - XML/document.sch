<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:title>ISO schematron description of a person</sch:title>
  <sch:pattern id="liste.checks">
    <sch:rule context="liste">
      <sch:assert test="count(personne) >= 1">Il doit y avoir au moins une personne.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern id="personne.checks">
    <sch:rule context="liste/personne">
      <sch:assert test="@id">Un departement doit porter un identifiant.</sch:assert>
      <sch:assert test="count(@id) = 1">L'identifiant doit etre unique.</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
