Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var baseAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/baseAvatar"));
// Constrain the number of visible suggestions
var MAX_SUGGESTIONS = 5;
var SuggestedAvatarStack = function (_a) {
    var owners = _a.owners, tooltip = _a.tooltip, tooltipOptions = _a.tooltipOptions, props = tslib_1.__rest(_a, ["owners", "tooltip", "tooltipOptions"]);
    var backgroundAvatarProps = tslib_1.__assign(tslib_1.__assign({}, props), { round: owners[0].type === 'user', suggested: true });
    var numAvatars = Math.min(owners.length, MAX_SUGGESTIONS);
    return (<AvatarStack>
      {tslib_1.__spreadArray([], tslib_1.__read(Array(numAvatars - 1))).map(function (_, i) { return (<BackgroundAvatar {...backgroundAvatarProps} key={i} type="background" index={i} hasTooltip={false}/>); })}
      <Avatar {...props} suggested actor={owners[0]} index={numAvatars - 1} tooltip={tooltip} tooltipOptions={tslib_1.__assign(tslib_1.__assign({}, tooltipOptions), { skipWrapper: true })}/>
    </AvatarStack>);
};
var AvatarStack = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-content: center;\n  flex-direction: row-reverse;\n"], ["\n  display: flex;\n  align-content: center;\n  flex-direction: row-reverse;\n"])));
var translateStyles = function (props) { return react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  transform: translateX(", "%);\n"], ["\n  transform: translateX(", "%);\n"])), 60 * props.index); };
var Avatar = styled_1.default(actorAvatar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), translateStyles);
var BackgroundAvatar = styled_1.default(baseAvatar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), translateStyles);
exports.default = SuggestedAvatarStack;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=suggestedAvatarStack.jsx.map