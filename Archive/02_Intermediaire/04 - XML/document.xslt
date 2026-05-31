<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
<xsl:output method="xml" indent="yes"/>
<xsl:param name="date" />
<xsl:template match="/">
    <root name='liste de personnes'>
        <xsl:attribute name="date">
            <xsl:value-of select="$date" />
        </xsl:attribute>
        <liste>
            <xsl:for-each select="//personne">
                <personne>
                    <nom>
                        <xsl:value-of select="@nom" />
                    </nom>
                </personne>
            </xsl:for-each>
        </liste>
    </root>
</xsl:template>
</xsl:stylesheet>
