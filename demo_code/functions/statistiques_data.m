function stats = statistiques_data(data)
% STATISTIQUES_DATA Statistiques descriptives pour un vecteur numérique.
%
% Calcule les mesures de tendance centrale et de dispersion pour un
% vecteur de valeurs numériques: moyenne, médiane, écart-type, minimum,
% maximum, étendue et nombre d'éléments. Retourne une structure regroupant
% ces indicateurs.
%
% :param data: Vecteur de données numériques à analyser.
%              Doit être un vecteur réel, non vide, avec valeurs finies.
% :type data: double (N×1 ou 1×N)
%
% :returns stats: Structure contenant les statistiques calculées.
% :rtype stats: struct avec champs
%               .moyenne, .mediane, .ecart_type, .minimum,
%               .maximum, .etendue, .nombre_elements
%
% Exemple:
%   data = [5, 15, 28, 12, 30, 8, 22];
%   stats = statistiques_data(data);
%   fprintf('Moyenne: %.2f\n', stats.moyenne);

    if ~isnumeric(data) || ~isvector(data)
        error('L''entrée doit être un vecteur numérique');
    end
    
    % Calcul des statistiques
    stats.moyenne = mean(data);
    stats.mediane = median(data);
    stats.ecart_type = std(data);
    stats.minimum = min(data);
    stats.maximum = max(data);
    stats.etendue = range(data);
    stats.nombre_elements = length(data);
end