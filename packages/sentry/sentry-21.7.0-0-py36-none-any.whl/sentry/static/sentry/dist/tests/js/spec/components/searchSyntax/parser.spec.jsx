Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var loadFixtures_1 = require("sentry-test/loadFixtures");
var parser_1 = require("app/components/searchSyntax/parser");
var utils_1 = require("app/components/searchSyntax/utils");
/**
 * Normalize results to match the json test cases
 */
var normalizeResult = function (tokens) {
    return utils_1.treeTransformer({
        tree: tokens,
        transform: function (token) {
            // XXX: This attempts to keep the test data simple, only including keys
            // that are really needed to validate functionality.
            // @ts-ignore
            delete token.location;
            // @ts-ignore
            delete token.text;
            // @ts-ignore
            delete token.config;
            if (token.type === parser_1.Token.Filter && token.invalid === null) {
                // @ts-ignore
                delete token.invalid;
            }
            if (token.type === parser_1.Token.ValueIso8601Date) {
                // Date values are represented as ISO strings in the test case json
                return tslib_1.__assign(tslib_1.__assign({}, token), { value: token.value.toISOString() });
            }
            return token;
        },
    });
};
describe('searchSyntax/parser', function () {
    var testData = loadFixtures_1.loadFixtures('search-syntax');
    var registerTestCase = function (testCase) {
        return it("handles " + testCase.query, function () {
            var result = parser_1.parseSearch(testCase.query);
            // Handle errors
            if (testCase.raisesError) {
                expect(result).toBeNull();
                return;
            }
            if (result === null) {
                throw new Error('Parsed result as null without raiseError true');
            }
            expect(normalizeResult(result)).toEqual(testCase.result);
        });
    };
    Object.entries(testData).map(function (_a) {
        var _b = tslib_1.__read(_a, 2), name = _b[0], cases = _b[1];
        return describe("" + name, function () {
            cases.map(registerTestCase);
        });
    });
});
//# sourceMappingURL=parser.spec.jsx.map