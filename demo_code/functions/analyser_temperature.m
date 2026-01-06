function resultat = analyser_temperature(temperatures)
% ANALYSER_TEMPERATURE Analyse et classification des températures.
%
% Calcule des statistiques descriptives sur un vecteur de températures
% (en °C) et classifie les éléments selon trois catégories: froid (<10°C),
% tempéré (10–25°C) et chaud (≥25°C). La sortie regroupe les statistiques
% globales et la répartition par catégorie.
%
% :param temperatures: Vecteur de températures en degrés Celsius.
%                      Les valeurs doivent être finies et réelles.
% :type temperatures: double (N×1 ou 1×N)
%
% :returns resultat: Structure d'analyse contenant statistiques et classification.
% :rtype resultat: struct avec champs
%                   .statistiques      (voir `statistiques_data`)
%                   .classification.froid
%                   .classification.tempere
%                   .classification.chaud
%                   .classification.pourcentage_chaud
%
% .. seealso:: `statistiques_data`
    
    stats = statistiques_data(temperatures);
    
    % Classification des températures
    nb_froid = sum(temperatures < 10);
    nb_tempere = sum(temperatures >= 10 & temperatures < 25);
    nb_chaud = sum(temperatures >= 25);
    
    % Construction du résultat
    resultat.statistiques = stats;
    resultat.classification.froid = nb_froid;
    resultat.classification.tempere = nb_tempere;
    resultat.classification.chaud = nb_chaud;
    resultat.classification.pourcentage_chaud = (nb_chaud / stats.nombre_elements) * 100;
end