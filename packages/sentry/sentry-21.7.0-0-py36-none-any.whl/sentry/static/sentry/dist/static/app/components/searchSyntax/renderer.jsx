Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var parser_1 = require("./parser");
var utils_1 = require("./utils");
/**
 * Renders the parsed query with syntax highlighting.
 */
function HighlightQuery(_a) {
    var parsedQuery = _a.parsedQuery, cursorPosition = _a.cursorPosition;
    var result = renderResult(parsedQuery, cursorPosition !== null && cursorPosition !== void 0 ? cursorPosition : -1);
    return <react_1.Fragment>{result}</react_1.Fragment>;
}
exports.default = HighlightQuery;
function renderResult(result, cursor) {
    return result
        .map(function (t) { return renderToken(t, cursor); })
        .map(function (renderedToken, i) { return <react_1.Fragment key={i}>{renderedToken}</react_1.Fragment>; });
}
function renderToken(token, cursor) {
    switch (token.type) {
        case parser_1.Token.Spaces:
            return token.value;
        case parser_1.Token.Filter:
            return <FilterToken filter={token} cursor={cursor}/>;
        case parser_1.Token.ValueTextList:
        case parser_1.Token.ValueNumberList:
            return <ListToken token={token} cursor={cursor}/>;
        case parser_1.Token.ValueNumber:
            return <NumberToken token={token}/>;
        case parser_1.Token.ValueBoolean:
            return <Boolean>{token.text}</Boolean>;
        case parser_1.Token.ValueIso8601Date:
            return <DateTime>{token.text}</DateTime>;
        case parser_1.Token.LogicGroup:
            return <LogicGroup>{renderResult(token.inner, cursor)}</LogicGroup>;
        case parser_1.Token.LogicBoolean:
            return <LogicBoolean>{token.value}</LogicBoolean>;
        default:
            return token.text;
    }
}
// XXX(epurkhiser): We have to animate `left` here instead of `transform` since
// inline elements cannot be transformed. The filter _must_ be inline to
// support text wrapping.
var shakeAnimation = react_2.keyframes(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), new Array(4)
    .fill(0)
    .map(function (_, i) { return i * (100 / 4) + "% { left: " + 3 * (i % 2 === 0 ? 1 : -1) + "px; }"; })
    .join('\n'));
var FilterToken = function (_a) {
    var _b;
    var filter = _a.filter, cursor = _a.cursor;
    var isActive = utils_1.isWithinToken(filter, cursor);
    // This state tracks if the cursor has left the filter token. We initialize it
    // to !isActive in the case where the filter token is rendered without the
    // cursor initally being in it.
    var _c = tslib_1.__read(react_1.useState(!isActive), 2), hasLeft = _c[0], setHasLeft = _c[1];
    // Used to trigger the shake animation when the element becomes invalid
    var filterElementRef = react_1.useRef(null);
    // Trigger the effect when isActive changes to updated whether the cursor has
    // left the token.
    react_1.useEffect(function () {
        if (!isActive && !hasLeft) {
            setHasLeft(true);
        }
    }, [isActive]);
    var showInvalid = hasLeft && !!filter.invalid;
    var showTooltip = showInvalid && isActive;
    var reduceMotion = framer_motion_1.useReducedMotion();
    // Trigger the shakeAnimation when showInvalid is set to true. We reset the
    // animation by clearing the style, set it to running, and re-applying the
    // animation
    react_1.useEffect(function () {
        if (!filterElementRef.current || !showInvalid || reduceMotion) {
            return;
        }
        var style = filterElementRef.current.style;
        style.animation = 'none';
        void filterElementRef.current.offsetTop;
        window.requestAnimationFrame(function () { return (style.animation = shakeAnimation.name + " 300ms"); });
    }, [showInvalid]);
    return (<tooltip_1.default disabled={!showTooltip} title={(_b = filter.invalid) === null || _b === void 0 ? void 0 : _b.reason} popperStyle={{ maxWidth: '350px' }} forceShow skipWrapper>
      <Filter ref={filterElementRef} active={isActive} invalid={showInvalid}>
        {filter.negated && <Negation>!</Negation>}
        <KeyToken token={filter.key} negated={filter.negated}/>
        {filter.operator && <Operator>{filter.operator}</Operator>}
        <Value>{renderToken(filter.value, cursor)}</Value>
      </Filter>
    </tooltip_1.default>);
};
var KeyToken = function (_a) {
    var token = _a.token, negated = _a.negated;
    var value = token.text;
    if (token.type === parser_1.Token.KeyExplicitTag) {
        value = (<ExplicitKey prefix={token.prefix}>
        {token.key.quoted ? "\"" + token.key.value + "\"" : token.key.value}
      </ExplicitKey>);
    }
    return <Key negated={!!negated}>{value}:</Key>;
};
var ListToken = function (_a) {
    var token = _a.token, cursor = _a.cursor;
    return (<InList>
    {token.items.map(function (_a) {
            var value = _a.value, separator = _a.separator;
            return [
                <ListComma key="comma">{separator}</ListComma>,
                renderToken(value, cursor),
            ];
        })}
  </InList>);
};
var NumberToken = function (_a) {
    var token = _a.token;
    return (<react_1.Fragment>
    {token.value}
    <Unit>{token.unit}</Unit>
  </react_1.Fragment>);
};
var colorType = function (p) {
    return "" + (p.invalid ? 'invalid' : 'valid') + (p.active ? 'Active' : '');
};
var Filter = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  --token-bg: ", ";\n  --token-border: ", ";\n  --token-value-color: ", ";\n\n  position: relative;\n  animation-name: ", ";\n"], ["\n  --token-bg: ", ";\n  --token-border: ", ";\n  --token-value-color: ", ";\n\n  position: relative;\n  animation-name: ", ";\n"])), function (p) { return p.theme.searchTokenBackground[colorType(p)]; }, function (p) { return p.theme.searchTokenBorder[colorType(p)]; }, function (p) { return (p.invalid ? p.theme.red300 : p.theme.blue300); }, shakeAnimation);
var filterCss = react_2.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: var(--token-bg);\n  border: 0.5px solid var(--token-border);\n  padding: ", " 0;\n"], ["\n  background: var(--token-bg);\n  border: 0.5px solid var(--token-border);\n  padding: ", " 0;\n"])), space_1.default(0.25));
var Negation = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"], ["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"])), filterCss, function (p) { return p.theme.red300; });
var Key = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ", ";\n"], ["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ", ";\n"])), filterCss, function (p) {
    return !p.negated
        ? react_2.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "], ["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "]))) : react_2.css(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n          border-left: none;\n          margin-left: 0;\n        "], ["\n          border-left: none;\n          margin-left: 0;\n        "])));
});
var ExplicitKey = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"], ["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.prefix; });
var Operator = styled_1.default('span')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"], ["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"])), filterCss, function (p) { return p.theme.orange400; });
var Value = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: var(--token-value-color);\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"], ["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: var(--token-value-color);\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"])), filterCss);
var Unit = styled_1.default('span')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var LogicBoolean = styled_1.default('span')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
var Boolean = styled_1.default('span')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.pink300; });
var DateTime = styled_1.default('span')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var ListComma = styled_1.default('span')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var InList = styled_1.default('span')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"], ["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, Value, function (p) { return p.theme.purple300; });
var LogicGroup = styled_1.default(function (_a) {
    var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
    return (<span {...props}>
    <span>(</span>
    {children}
    <span>)</span>
  </span>);
})(templateObject_17 || (templateObject_17 = tslib_1.__makeTemplateObject(["\n  > span:first-child,\n  > span:last-child {\n    position: relative;\n    color: transparent;\n\n    &:before {\n      position: absolute;\n      top: -5px;\n      color: ", ";\n      font-size: 16px;\n      font-weight: bold;\n    }\n  }\n\n  > span:first-child:before {\n    left: -3px;\n    content: '(';\n  }\n  > span:last-child:before {\n    right: -3px;\n    content: ')';\n  }\n"], ["\n  > span:first-child,\n  > span:last-child {\n    position: relative;\n    color: transparent;\n\n    &:before {\n      position: absolute;\n      top: -5px;\n      color: ", ";\n      font-size: 16px;\n      font-weight: bold;\n    }\n  }\n\n  > span:first-child:before {\n    left: -3px;\n    content: '(';\n  }\n  > span:last-child:before {\n    right: -3px;\n    content: ')';\n  }\n"])), function (p) { return p.theme.orange400; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=renderer.jsx.map