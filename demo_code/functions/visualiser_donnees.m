function visualiser_donnees(data, titre)
% VISUALISER_DONNEES Visualisations d'un vecteur de données.
%
% Affiche une figure avec quatre sous-graphes: histogramme, boxplot,
% courbe d'évolution (index en abscisse) et statistiques textuelles.
% Le titre de la fenêtre est optionnel.
%
% :param data: Vecteur de valeurs numériques à visualiser. Les valeurs
%              doivent être finies (sans NaN/Inf).
% :type data: double (N×1 ou 1×N)
% :param titre: Titre de la figure (optionnel). Valeur par défaut:
%               'Visualisation des données'.
% :type titre: char|string
%
% :returns: Aucune sortie. Crée une figure avec quatre sous-graphes.
% :rtype: void
%
% Exemple:
%   data = randn(100,1);
%   visualiser_donnees(data, 'Données simulées');
%
% .. seealso:: `statistiques_data`
    
    if nargin < 2
        titre = 'Visualisation des données';
    end
    
    figure('Name', titre, 'NumberTitle', 'off');
    
    % Sous-graphique 1: Histogramme
    subplot(2, 2, 1);
    histogram(data, 15, 'FaceColor', [0.2 0.5 0.8]);
    title('Distribution des données');
    xlabel('Valeur');
    ylabel('Fréquence');
    grid on;
    
    % Sous-graphique 2: Box plot
    subplot(2, 2, 2);
    boxplot(data);
    title('Box Plot');
    ylabel('Valeur');
    grid on;
    
    % Sous-graphique 3: Évolution temporelle
    subplot(2, 2, 3);
    plot(1:length(data), data, '-o', 'LineWidth', 1.5, 'MarkerSize', 4);
    title('Évolution temporelle');
    xlabel('Index');
    ylabel('Valeur');
    grid on; %#BUG complexifier les graphes
    
    % Sous-graphique 4: Statistiques textuelles
    subplot(2, 2, 4);
    stats = statistiques_data(data);
    text_stats = sprintf(...
        'Moyenne: %.2f\nMédiane: %.2f\nÉcart-type: %.2f\nMin: %.2f\nMax: %.2f', ...
        stats.moyenne, stats.mediane, stats.ecart_type, stats.minimum, stats.maximum);
    text(0.1, 0.5, text_stats, 'FontSize', 11, 'VerticalAlignment', 'middle');
    axis off;
    title('Statistiques');
end