Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var utils_1 = require("app/utils");
var Context = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline;\n"], ["\n  display: inline;\n"])));
var ContextLine = function (props) {
    var _a;
    var line = props.line, isActive = props.isActive, className = props.className;
    var lineWs = '';
    var lineCode = '';
    if (utils_1.defined(line[1]) && line[1].match) {
        _a = tslib_1.__read(line[1].match(/^(\s*)(.*?)$/m), 3), lineWs = _a[1], lineCode = _a[2];
    }
    var Component = !props.children ? React.Fragment : Context;
    return (<li className={classnames_1.default(className, 'expandable', { active: isActive })} key={line[0]}>
      <Component>
        <span className="ws">{lineWs}</span>
        <span className="contextline">{lineCode}</span>
      </Component>
      {props.children}
    </li>);
};
exports.default = ContextLine;
var templateObject_1;
//# sourceMappingURL=contextLine.jsx.map