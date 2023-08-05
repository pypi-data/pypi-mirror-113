Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var line_1 = tslib_1.__importDefault(require("app/components/events/interfaces/frame/line"));
var locale_1 = require("app/locale");
var TemplateInterface = function (_a) {
    var type = _a.type, data = _a.data, event = _a.event;
    return (<eventDataSection_1.default type={type} title={locale_1.t('Template')}>
    <div className="traceback no-exception">
      <ul>
        <line_1.default data={data} event={event} registers={{}} components={[]} isExpanded/>
      </ul>
    </div>
  </eventDataSection_1.default>);
};
exports.default = TemplateInterface;
//# sourceMappingURL=template.jsx.map