Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var contextSummaryDevice_1 = tslib_1.__importDefault(require("./contextSummaryDevice"));
var contextSummaryGeneric_1 = tslib_1.__importDefault(require("./contextSummaryGeneric"));
var contextSummaryGPU_1 = tslib_1.__importDefault(require("./contextSummaryGPU"));
var contextSummaryOS_1 = tslib_1.__importDefault(require("./contextSummaryOS"));
var contextSummaryUser_1 = tslib_1.__importDefault(require("./contextSummaryUser"));
var filterContexts_1 = tslib_1.__importDefault(require("./filterContexts"));
var MIN_CONTEXTS = 3;
var MAX_CONTEXTS = 4;
var KNOWN_CONTEXTS = [
    { keys: ['user'], Component: contextSummaryUser_1.default },
    {
        keys: ['browser'],
        Component: contextSummaryGeneric_1.default,
        unknownTitle: locale_1.t('Unknown Browser'),
    },
    {
        keys: ['runtime'],
        Component: contextSummaryGeneric_1.default,
        unknownTitle: locale_1.t('Unknown Runtime'),
    },
    { keys: ['client_os', 'os'], Component: contextSummaryOS_1.default },
    { keys: ['device'], Component: contextSummaryDevice_1.default },
    { keys: ['gpu'], Component: contextSummaryGPU_1.default },
];
var ContextSummary = /** @class */ (function (_super) {
    tslib_1.__extends(ContextSummary, _super);
    function ContextSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ContextSummary.prototype.render = function () {
        var event = this.props.event;
        var contextCount = 0;
        // Add defined contexts in the declared order, until we reach the limit
        // defined by MAX_CONTEXTS.
        var contexts = KNOWN_CONTEXTS.filter(function (context) { return filterContexts_1.default(event, context); }).map(function (_a) {
            var keys = _a.keys, Component = _a.Component, unknownTitle = _a.unknownTitle;
            if (contextCount >= MAX_CONTEXTS) {
                return null;
            }
            var _b = tslib_1.__read(keys
                .map(function (k) { return [k, event.contexts[k] || event[k]]; })
                .find(function (_a) {
                var _b = tslib_1.__read(_a, 2), _k = _b[0], d = _b[1];
                return !utils_1.objectIsEmpty(d);
            }) || [null, null], 2), key = _b[0], data = _b[1];
            if (!key) {
                return null;
            }
            contextCount += 1;
            return <Component key={key} data={data} unknownTitle={unknownTitle}/>;
        });
        // Bail out if all contexts are empty or only the user context is set
        if (contextCount === 0 || (contextCount === 1 && contexts[0])) {
            return null;
        }
        if (contextCount < MIN_CONTEXTS) {
            // Add contents in the declared order until we have at least MIN_CONTEXTS
            // contexts in our list.
            contexts = KNOWN_CONTEXTS.filter(function (context) { return filterContexts_1.default(event, context); }).map(function (_a, index) {
                var keys = _a.keys, Component = _a.Component, unknownTitle = _a.unknownTitle;
                if (contexts[index]) {
                    return contexts[index];
                }
                if (contextCount >= MIN_CONTEXTS) {
                    return null;
                }
                contextCount += 1;
                return <Component key={keys[0]} data={{}} unknownTitle={unknownTitle}/>;
            });
        }
        return <Wrapper className="context-summary">{contexts}</Wrapper>;
    };
    return ContextSummary;
}(React.Component));
exports.default = ContextSummary;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    display: flex;\n    gap: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    display: flex;\n    gap: ", ";\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(3), space_1.default(2));
var templateObject_1;
//# sourceMappingURL=contextSummary.jsx.map