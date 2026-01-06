%% ILLUSTRATION DES FONCTIONNALITÉS MATLAB DANS VSCODE

%% Nettoyage de l'environnement
% clear all;
% close all;
% clc;
set(0, 'DefaultFigureVisible', 'on');

%% 1. Génération de données de température
fprintf('1. Génération de données de température...\n');

% Simulation de températures sur 30 jours
rng(42); % Pour reproductibilité

temperatures = 15 + 10 * randn(1, 30); % Températures autour de 15°C

fprintf('   Nombre de mesures: %d jours\n\n', length(temperatures));

%% 2. Calcul des statistiques de base
fprintf('2. Calcul des statistiques de base...\n');

stats = statistiques_data(temperatures);

fprintf('   Moyenne: %.2f°C\n', stats.moyenne);
fprintf('   Médiane: %.2f°C\n', stats.mediane);
fprintf('   Écart-type: %.2f°C\n', stats.ecart_type);
fprintf('   Étendue: [%.2f°C, %.2f°C]\n\n', stats.minimum, stats.maximum);

%% 3. Analyse détaillée des températures
fprintf('3. Analyse détaillée des températures...\n');

analyse = analyser_temperature(temperatures);


fprintf('   Jours froids (< 10°C): %d\n', analyse.classification.froid);
fprintf('   Jours tempérés (10-25°C): %d\n', analyse.classification.tempere);
fprintf('   Jours chauds (>= 25°C): %d\n', analyse.classification.chaud);
fprintf('   Pourcentage de jours chauds: %.1f%%\n\n', analyse.classification.pourcentage_chaud);

%% 4. Visualisation des données
fprintf('4. Création des visualisations...\n');

visualiser_donnees(temperatures, 'Analyse des Températures sur 30 jours');

fprintf('   Graphiques créés avec succès!\n\n');

%% Fin du script
fprintf('\n=== FIN DU SCRIPT ===\n');
fprintf('Toutes les fonctions ont été exécutées avec succès\n');

% Useful tools
% # TODO jeu de données à complexifier
% #BUG fonction analyser_temperature ne gère pas les NaN
% #FIXME ajouter gestion des erreurs dans statistiques_data