classdef TestStatistiquesData < matlab.unittest.TestCase
    % TESTSTATISTIQUESDATA Suite de tests pour `statistiques_data`.
    %
    % Valide la structure de sortie et l'exactitude des mesures
    % statistiques calculées par la fonction `statistiques_data` avec
    % différents cas (vecteurs ligne/colonne, valeurs négatives,
    % décimales, un seul élément, consistance, exemple documentation).
    %
    % :param data: Données utilisées dans les tests (chaque méthode définit son jeu).
    % :type data: double (N×1 ou 1×N)
    %
    % :returns: Aucune sortie (classe de tests unitaires).
    % :rtype: `matlab.unittest.TestCase`
    %
    % .. seealso:: `statistiques_data`, `matlab.unittest`
    
    methods(Test)
        
        function testStructureSortie(testCase)
            % Test que la fonction retourne une structure avec tous les champs requis
            data = [15, 20, 25]';
            stats = statistiques_data(data);
            
            % Vérifier que le résultat est une structure
            testCase.verifyTrue(isstruct(stats), ...
                'Le résultat doit être une structure');
            
            % Vérifier la présence de tous les champs requis
            champs_requis = {'moyenne', 'mediane', 'ecart_type', 'minimum', ...
                           'maximum', 'etendue', 'nombre_elements'};
            
            for i = 1:length(champs_requis)
                testCase.verifyTrue(isfield(stats, champs_requis{i}), ...
                    sprintf('Le champ %s doit exister', champs_requis{i}));
            end
        end
        
        function testCalculsStatistiques(testCase)
            % Test des calculs statistiques avec des données connues
            data = [10, 20, 30]';
            stats = statistiques_data(data);
            
            % Vérifier les calculs (valeurs attendues connues)
            testCase.verifyEqual(stats.moyenne, 20, 'AbsTol', 1e-10, ...
                'La moyenne doit être correcte');
            testCase.verifyEqual(stats.mediane, 20, 'AbsTol', 1e-10, ...
                'La médiane doit être correcte');
            testCase.verifyEqual(stats.minimum, 10, ...
                'Le minimum doit être correct');
            testCase.verifyEqual(stats.maximum, 30, ...
                'Le maximum doit être correct');
            testCase.verifyEqual(stats.etendue, 20, ...
                'L''étendue doit être correcte');
            testCase.verifyEqual(stats.nombre_elements, 3, ...
                'Le nombre d''éléments doit être correct');
        end
        
        function testVecteurLigne(testCase)
            % Test avec un vecteur ligne
            data = [5, 15, 25]; % Vecteur ligne
            stats = statistiques_data(data);
            
            % Vérifier que la fonction fonctionne avec des vecteurs lignes
            testCase.verifyEqual(stats.nombre_elements, 3, ...
                'La fonction doit fonctionner avec des vecteurs lignes');
            testCase.verifyEqual(stats.moyenne, 15, 'AbsTol', 1e-10);
        end
        
        function testVecteurColonne(testCase)
            % Test avec un vecteur colonne
            data = [5; 15; 25]; % Vecteur colonne
            stats = statistiques_data(data);
            
            % Vérifier que la fonction fonctionne avec des vecteurs colonnes
            testCase.verifyEqual(stats.nombre_elements, 3, ...
                'La fonction doit fonctionner avec des vecteurs colonnes');
            testCase.verifyEqual(stats.moyenne, 15, 'AbsTol', 1e-10);
        end
        
        function testUnSeulElement(testCase)
            % Test avec un seul élément
            data = 42;
            stats = statistiques_data(data);
            
            testCase.verifyEqual(stats.moyenne, 42);
            testCase.verifyEqual(stats.mediane, 42);
            testCase.verifyEqual(stats.minimum, 42);
            testCase.verifyEqual(stats.maximum, 42);
            testCase.verifyEqual(stats.etendue, 0);
            testCase.verifyEqual(stats.nombre_elements, 1);
        end
        
        function testValeursNegatives(testCase)
            % Test avec des valeurs négatives
            data = [-10, -5, 0, 5, 10];
            stats = statistiques_data(data);
            
            testCase.verifyEqual(stats.moyenne, 0, 'AbsTol', 1e-10);
            testCase.verifyEqual(stats.mediane, 0);
            testCase.verifyEqual(stats.minimum, -10);
            testCase.verifyEqual(stats.maximum, 10);
            testCase.verifyEqual(stats.etendue, 20);
        end
        
        function testValeursDecimales(testCase)
            % Test avec des nombres décimaux
            data = [1.5, 2.7, 3.1, 4.8];
            stats = statistiques_data(data);
            
            % Vérifier que tous les champs sont numériques
            testCase.verifyTrue(isnumeric(stats.moyenne));
            testCase.verifyTrue(isnumeric(stats.mediane));
            testCase.verifyTrue(isnumeric(stats.ecart_type));
            
            % Vérifier quelques calculs
            testCase.verifyEqual(stats.nombre_elements, 4);
            testCase.verifyEqual(stats.minimum, 1.5);
            testCase.verifyEqual(stats.maximum, 4.8);
        end
        
        function testTypesSortie(testCase)
            % Test des types de données en sortie
            data = [10, 20, 30]';
            stats = statistiques_data(data);
            
            % Vérifier que stats est bien une structure
            testCase.verifyClass(stats, 'struct', ...
                'Le résultat doit être de type struct');
            
            % Vérifier que tous les champs sont numériques
            champs = fieldnames(stats);
            for i = 1:length(champs)
                testCase.verifyTrue(isnumeric(stats.(champs{i})), ...
                    sprintf('Le champ %s doit être numérique', champs{i}));
            end
        end
        
        function testConsistance(testCase)
            % Test de consistance : appels multiples avec mêmes données
            data = [12, 18, 24]';
            
            % Appeler la fonction plusieurs fois
            stats1 = statistiques_data(data);
            stats2 = statistiques_data(data);
            
            % Les résultats doivent être identiques
            testCase.verifyEqual(stats1, stats2, ...
                'Les appels multiples avec les mêmes données doivent donner le même résultat');
        end
        
        
        function testExempleDocumentation(testCase)
            % Test avec l'exemple donné dans la documentation
            data = [5, 15, 28, 12, 30, 8, 22];
            stats = statistiques_data(data);
            
            % Vérifier que l'exemple fonctionne
            testCase.verifyEqual(stats.nombre_elements, 7);
            testCase.verifyTrue(stats.moyenne > 0);
            testCase.verifyEqual(stats.minimum, 5);
            testCase.verifyEqual(stats.maximum, 30);
            
            % Vérifier que la moyenne calculée est cohérente
            moyenne_attendue = sum(data) / length(data);
            testCase.verifyEqual(stats.moyenne, moyenne_attendue, 'AbsTol', 1e-10);
        end
    end
    
    methods(TestMethodSetup)
        function setupTest(testCase)
            % Vérifier que la fonction statistiques_data existe
            if ~exist('statistiques_data', 'file')
                error('La fonction statistiques_data doit être disponible pour les tests');
            end
        end
    end
end
