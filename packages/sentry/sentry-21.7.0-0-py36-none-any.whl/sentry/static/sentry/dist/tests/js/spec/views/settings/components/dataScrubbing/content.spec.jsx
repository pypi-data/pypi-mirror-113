Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var content_1 = tslib_1.__importDefault(require("app/views/settings/components/dataScrubbing/content"));
var convertRelayPiiConfig_1 = tslib_1.__importDefault(require("app/views/settings/components/dataScrubbing/convertRelayPiiConfig"));
// @ts-expect-error
var relayPiiConfig = TestStubs.DataScrubbingRelayPiiConfig();
var stringRelayPiiConfig = JSON.stringify(relayPiiConfig);
var convertedRules = convertRelayPiiConfig_1.default(stringRelayPiiConfig);
var handleEditRule = jest.fn();
var handleDelete = jest.fn();
describe('Content', function () {
    it('default render - empty', function () {
        var wrapper = enzyme_1.mountWithTheme(<content_1.default rules={[]} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.text()).toEqual('You have no data scrubbing rules');
    });
    it('render rules', function () {
        var wrapper = enzyme_1.mountWithTheme(<content_1.default rules={convertedRules} onEditRule={handleEditRule} onDeleteRule={handleDelete}/>);
        expect(wrapper.find('List')).toHaveLength(1);
    });
});
//# sourceMappingURL=content.spec.jsx.map